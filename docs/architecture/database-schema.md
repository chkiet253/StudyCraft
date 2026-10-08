# StudyCraft — Thiết kế schema PostgreSQL MVP

> **Chưa đồng bộ SPEC v3 (2026-10-08):** DDL bên dưới vẫn là baseline trước quyết định lưu chat và giới hạn từ theo loại bài. Các quy tắc 16 bảng/chat RAM/trần 300 từ đã bị thay thế bởi [SPEC §6/§9](../SPEC.md). I-03/I-05 phải bổ sung policy snapshot, chat_threads/chat_messages, constraints và indexes trước khi dùng DDL này để triển khai.

**Status: Proposed — 2026-10-07.** Nguồn: [PRD](../requirements/prd.md), [US-001–US-018](../requirements/user-stories.md), [system design](system-design.md), [SPEC §6/§9](../SPEC.md), [ADR 002](adr/002-postgres-durable-records.md) và [ADR 005](adr/005-ephemeral-chat-versioned-journals.md). Đây là thiết kế bàn giao, chưa phải migration đã chạy.

**Bổ sung HTTP contract — 2026-10-08:** [OpenAPI đề xuất](../api/openapi.json) ánh xạ Idempotency-Key → request_id nội bộ và Problem → Error metadata; bổ sung INTERNAL_ERROR/HTTP 500 cho receipt/run đã claim. Lỗi transport 400/405/413/415 bị chặn trước claim, không lưu receipt. Chưa có migration thực thi.

## 1. Phạm vi, giả định và thay đổi hợp đồng cần chốt

- Giữ đúng 16 bảng trong SPEC. Một người học, một workspace tiếng Anh, model local; không bảng users/roles, billing, files, embeddings hoặc transcript.
- DDL dưới đây đề xuất PostgreSQL 16 trở lên; phiên bản triển khai cụ thể: `TODO(developer)`. Không cần extension. UUID v4 do ứng dụng sinh; ngoại trừ history ID, không có default sinh ID trong DB.
- Mọi cột không có DEFAULT phải được caller cung cấp nếu NOT NULL. Cột nullable không có DEFAULT mặc định NULL. `updated_at` do service cập nhật trong cùng transaction; DEFAULT chỉ áp dụng lúc INSERT.
- Timestamps dùng `timestamptz`; API xuất ISO 8601. Ngày nghiệp vụ dùng `date`, timezone `Asia/Ho_Chi_Minh`, tuần thứ Hai–Chủ nhật theo giả định SPEC A05. Không chuyển bài gốc sang dạng đã trim/normalize.
- Giới hạn từ/ký tự/nguồn kế thừa các giả định SPEC; không phải chuẩn TOEIC/IELTS. VARCHAR giới hạn ký tự, không phải UTF-8 bytes; giới hạn context bytes kiểm ở ứng dụng.
- **US-003 — đã đồng bộ thiết kế ở P01:** planned_period: day|week có mặc định day. OpenAPI ActivityInputData cho phép bỏ trường này; adapter phải điền day trước hash/gọi tool. SPEC ActivityData nội bộ và HTTP output bắt buộc có planned_period. Với week, planned_for là thứ Hai; NULL ngày là chưa lên lịch. Frontend/tests triển khai theo cùng contract; không âm thầm hiểu mọi ngày thứ Hai là việc theo tuần. Chưa có implementation.
- **Bổ sung nội bộ DB:** các FK có `workspace_id`; typed entity references cho events/history; `requests.error_code/error_retryable`; `runs.context_truncated`. Không thêm trường công khai ngoài thay đổi ActivityData nêu trên.
- Tên `entity_id` vẫn có trong API/SPEC; DB sinh từ đúng một typed reference. JSON source-ID lists giữ theo SPEC, được kiểm tồn tại/phạm vi bằng service; chúng không có FK từng phần tử.

**Truy vết:** US-001 → workspaces; US-002 → catalog_materials/materials; US-003–004 → activities/learning_events; US-005 → writing_templates/exercises; US-006/010 → submissions; US-007–009 → feedback/requests/runs và material snapshot; US-011 → history_index/artifacts; US-012–013/017 → runs/requests/learning_reports, chat RAM; US-014–016 → journals/revisions/corrections/events/reports; US-018 → scoped FK, quyền service và quyền DB.

## 2. Bảng, cột, kiểu, constraints và defaults

SQL định nghĩa cấu trúc đề xuất. Tạo theo thứ tự dưới đây trong một migration transaction. Mọi FK mặc định NO ACTION, không ON DELETE CASCADE. PK/UNIQUE là khóa chính/ràng buộc không trùng; FK là khóa ngoại. CHECK kiểm điều kiện trong một hàng; điều kiện nhiều hàng và JSON schema đầy đủ được ghi ở mục 4. [PostgreSQL constraints](https://www.postgresql.org/docs/current/ddl-constraints.html).

### 2.1. workspaces — hồ sơ/mục tiêu do người học lưu

```sql
CREATE TABLE workspaces (
    id uuid PRIMARY KEY,
    subject text NOT NULL DEFAULT 'english' UNIQUE CHECK (subject = 'english'),
    method text NOT NULL DEFAULT 'short_writing' CHECK (method = 'short_writing'),
    goal_text varchar(400),
    deadline date,
    study_context varchar(4000) NOT NULL DEFAULT '',
    learner_profile jsonb NOT NULL DEFAULT
        '{"self_reported_level":"unknown","writing_purpose":"","writing_type":"general_paragraph"}'::jsonb,
    version bigint NOT NULL DEFAULT 0 CHECK (version >= 0),
    updated_at timestamptz NOT NULL DEFAULT now(),
    CHECK (goal_text IS NULL OR length(btrim(goal_text)) > 0),
    CHECK (goal_text IS NOT NULL OR deadline IS NULL),
    CHECK (jsonb_typeof(learner_profile) = 'object'),
    CHECK (learner_profile ?& ARRAY['self_reported_level','writing_purpose','writing_type'])
);
```

`goal_text=NULL, deadline=NULL` → API goal=null. Có mục tiêu nhưng chưa hạn → deadline=NULL. Trình độ mặc định unknown; không lưu điểm suy ra từ bài. UNIQUE subject cố ý giới hạn một workspace MVP.

### 2.2. catalog_materials — tài liệu mẫu developer cung cấp

```sql
CREATE TABLE catalog_materials (
    id uuid PRIMARY KEY,
    title varchar(200) NOT NULL CHECK (length(btrim(title)) > 0),
    description varchar(1000) NOT NULL DEFAULT '',
    content varchar(20000) CHECK (content IS NULL OR length(btrim(content)) > 0),
    updated_at timestamptz NOT NULL DEFAULT now()
);
```

Tối đa 100 seed items theo SPEC; `has_content` của API được tính từ `content IS NOT NULL`. Không suy đoán nội dung từ title.

### 2.3. writing_templates — đề mẫu

```sql
CREATE TABLE writing_templates (
    id uuid PRIMARY KEY,
    prompt varchar(2000) NOT NULL CHECK (length(btrim(prompt)) > 0)
);
```

Tối đa 20 seed items. Chỉ migration/seed owner ghi; runtime đọc.

### 2.4. materials — bản tài liệu trong workspace

```sql
CREATE TABLE materials (
    id uuid PRIMARY KEY,
    workspace_id uuid NOT NULL REFERENCES workspaces(id),
    catalog_id uuid REFERENCES catalog_materials(id),
    title varchar(200) NOT NULL CHECK (length(btrim(title)) > 0),
    description varchar(1000) NOT NULL DEFAULT '',
    content varchar(20000) CHECK (content IS NULL OR length(btrim(content)) > 0),
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (workspace_id, id),
    UNIQUE (workspace_id, catalog_id),
    CHECK (updated_at >= created_at)
);
```

UNIQUE vẫn cho nhiều catalog_id=NULL. Chọn danh mục tạo bản sao; chọn lại trả bản hiện có. Sửa thành tài liệu tự nhập đặt catalog_id=NULL. Giới hạn 50/workspace kiểm dưới khóa workspace.

### 2.5. activities — việc dự định học và trạng thái tự xác nhận

```sql
CREATE TABLE activities (
    id uuid PRIMARY KEY,
    workspace_id uuid NOT NULL REFERENCES workspaces(id),
    title varchar(300) NOT NULL CHECK (length(btrim(title)) > 0),
    planned_period text NOT NULL DEFAULT 'day' CHECK (planned_period IN ('day','week')),
    planned_for date,
    status text NOT NULL DEFAULT 'planned' CHECK (status IN ('planned','completed','deferred')),
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (workspace_id, id),
    CHECK (planned_for IS NULL OR planned_period <> 'week'
           OR extract(isodow FROM planned_for) = 1),
    CHECK (updated_at >= created_at)
);
```

planned_period theo contract đã đồng bộ ở mục 1. Status chỉ thay theo thao tác trực tiếp. Không có auto-complete khi nhận feedback.

### 2.6. requests — receipt cho thao tác ghi và idempotency

```sql
CREATE TABLE requests (
    workspace_id uuid NOT NULL REFERENCES workspaces(id),
    request_id uuid NOT NULL,
    tool text NOT NULL CHECK (tool IN (
        'workspace.update','material.save','activity.save','exercise.create',
        'submission.add','feedback.generate','chat.send','journal.summarize','journal.correct')),
    payload_hash text NOT NULL CHECK (payload_hash ~ '^[0-9a-f]{64}$'),
    state text NOT NULL DEFAULT 'in_progress' CHECK (state IN ('in_progress','completed')),
    http_status smallint,
    error_code varchar(50),
    error_retryable boolean NOT NULL DEFAULT false,
    response_json jsonb,
    result_ids uuid[] NOT NULL DEFAULT '{}'::uuid[],
    created_at timestamptz NOT NULL DEFAULT now(),
    completed_at timestamptz,
    PRIMARY KEY (workspace_id, request_id),
    UNIQUE (workspace_id, request_id, tool),
    CHECK (cardinality(result_ids) <= 4),
    CHECK (array_position(result_ids, NULL) IS NULL),
    CHECK (response_json IS NULL OR jsonb_typeof(response_json) = 'object'),
    CHECK (tool <> 'chat.send' OR response_json IS NULL),
    CHECK ((state = 'in_progress' AND http_status IS NULL AND completed_at IS NULL
            AND error_code IS NULL AND response_json IS NULL AND cardinality(result_ids) = 0)
        OR (state = 'completed' AND http_status IS NOT NULL AND completed_at IS NOT NULL
            AND completed_at >= created_at)),
    CHECK (http_status IS NULL OR http_status IN (200,403,404,409,422,500,502,503,504)),
    CHECK (state <> 'completed' OR
        (http_status = 200 AND error_code IS NULL AND NOT error_retryable
         AND (tool = 'chat.send' OR response_json IS NOT NULL)) OR
        (http_status <> 200 AND error_code IS NOT NULL AND response_json IS NULL
         AND cardinality(result_ids) = 0))
);
```

Idempotency là gửi lại cùng yêu cầu mà không tạo thêm tác động. Hash = SHA-256(tool + canonical input bỏ request_id). Không lưu input. Thành công non-chat lưu đúng response artifact đã validate, gồm journal revision cụ thể; replay không đọc nhầm bản mới. Journal replay trả response ban đầu, kể cả status lúc đó; đọc artifact bình thường tính lại current/stale theo nguồn hiện tại. Chat thành công chỉ giữ IDs reports; reply ở RAM. Lỗi chỉ lưu code/retryable/status, message dựng từ danh sách an toàn; không cache đoạn chat, question hoặc provider error text trong DB.

Error.run_id được dựng bằng cách tìm runs có cùng workspace_id/request_id: có run → dùng request UUID, chưa tạo run → NULL. RUN_BUSY của một UUID mới không trả ID run của request khác. Replay lỗi giữ code/retryable/run_id/http_status; message an toàn có thể khác câu hỏi làm rõ trả tạm lần đầu. Đây là quy tắc replay đề xuất cần ghi rõ trong service/tests, không cam kết lưu nguyên văn câu hỏi model.

### 2.7. runs — metadata một lượt xử lý bằng model

```sql
CREATE TABLE runs (
    id uuid PRIMARY KEY,
    workspace_id uuid NOT NULL REFERENCES workspaces(id),
    operation text NOT NULL CHECK (operation IN
        ('feedback.generate','chat.send','journal.summarize','journal.correct')),
    status text NOT NULL DEFAULT 'running' CHECK (status IN
        ('running','succeeded','failed','interrupted')),
    model varchar(200),
    prompt_version varchar(100) NOT NULL CHECK (length(btrim(prompt_version)) > 0),
    attempts smallint NOT NULL DEFAULT 0 CHECK (attempts BETWEEN 0 AND 2),
    input_tokens bigint CHECK (input_tokens >= 0),
    output_tokens bigint CHECK (output_tokens >= 0),
    context_truncated boolean NOT NULL DEFAULT false,
    context_metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
    error_code varchar(50),
    result_ids uuid[] NOT NULL DEFAULT '{}'::uuid[],
    started_at timestamptz NOT NULL DEFAULT now(),
    finished_at timestamptz,
    UNIQUE (workspace_id, id),
    FOREIGN KEY (workspace_id, id, operation)
        REFERENCES requests(workspace_id, request_id, tool),
    CHECK (model IS NULL OR length(btrim(model)) > 0),
    CHECK (jsonb_typeof(context_metadata) = 'object'),
    CHECK (cardinality(result_ids) <= 4),
    CHECK (array_position(result_ids, NULL) IS NULL),
    CHECK ((status = 'running' AND finished_at IS NULL AND error_code IS NULL
            AND cardinality(result_ids) = 0)
        OR (status = 'succeeded' AND finished_at IS NOT NULL AND error_code IS NULL)
        OR (status IN ('failed','interrupted') AND finished_at IS NOT NULL
            AND error_code IS NOT NULL AND cardinality(result_ids) = 0)),
    CHECK (finished_at IS NULL OR finished_at >= started_at)
);
```

id=request_id theo SPEC. `context_metadata` chỉ chứa allowlist IDs, revision, signature, byte_count và cấu hình giới hạn; không raw text. Tokens NULL nếu runtime không báo; NULL khác 0. Attempts tăng trước mỗi HTTP attempt, cả hai trong deadline 120 giây. result_ids: feedback ID; chat report IDs; hoặc journal ID. Journal revision chính xác nằm trong receipt response, không suy ra từ journal ID.

### 2.8. exercises — snapshot của đề và tài liệu lúc tạo đề

```sql
CREATE TABLE exercises (
    id uuid PRIMARY KEY,
    workspace_id uuid NOT NULL REFERENCES workspaces(id),
    prompt varchar(2000) NOT NULL CHECK (length(btrim(prompt)) > 0),
    origin text NOT NULL CHECK (origin IN ('user','template')),
    template_id uuid REFERENCES writing_templates(id),
    material_id uuid,
    material_snapshot jsonb,
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (workspace_id, id),
    FOREIGN KEY (workspace_id, material_id) REFERENCES materials(workspace_id, id),
    CHECK ((origin = 'user' AND template_id IS NULL)
        OR (origin = 'template' AND template_id IS NOT NULL)),
    CHECK ((material_id IS NULL AND material_snapshot IS NULL)
        OR (material_id IS NOT NULL AND material_snapshot IS NOT NULL
            AND jsonb_typeof(material_snapshot) = 'object'))
);
```

Immutable — bất biến sau INSERT. material_snapshot là toàn bộ Material theo JSON contract, cùng ID/phạm vi, kể cả content=NULL. Đổi tài liệu/đề mẫu sau này không đổi đề hoặc nguồn của bài cũ.

### 2.9. submissions — bài gốc và bản viết lại

```sql
CREATE TABLE submissions (
    id uuid PRIMARY KEY,
    workspace_id uuid NOT NULL REFERENCES workspaces(id),
    exercise_id uuid NOT NULL,
    revision_of uuid,
    text varchar(6000) NOT NULL CHECK (length(btrim(text)) > 0),
    word_count smallint NOT NULL CHECK (word_count BETWEEN 1 AND 300),
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (workspace_id, id),
    UNIQUE (workspace_id, exercise_id, id),
    FOREIGN KEY (workspace_id, exercise_id) REFERENCES exercises(workspace_id, id),
    FOREIGN KEY (workspace_id, exercise_id, revision_of)
        REFERENCES submissions(workspace_id, exercise_id, id),
    CHECK (revision_of IS NULL OR revision_of <> id)
);
```

Immutable. Bản viết lại trỏ bài cha trực tiếp đã tồn tại, cùng exercise/workspace; có thể nhiều nhánh. Không thay text bằng corrected_text. Regex đếm từ và offsets Unicode theo SPEC kiểm bằng Python, không dùng số do client/model gửi.

### 2.10. feedback — bản sửa hợp lệ, tách khỏi bài gốc

```sql
CREATE TABLE feedback (
    id uuid PRIMARY KEY,
    workspace_id uuid NOT NULL REFERENCES workspaces(id),
    submission_id uuid NOT NULL,
    run_id uuid NOT NULL UNIQUE,
    rubric_version text NOT NULL DEFAULT 'correction-v2' CHECK (rubric_version = 'correction-v2'),
    data jsonb NOT NULL,
    corrected_text varchar(10000) NOT NULL CHECK (length(corrected_text) > 0),
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (workspace_id, id),
    FOREIGN KEY (workspace_id, submission_id) REFERENCES submissions(workspace_id, id),
    FOREIGN KEY (workspace_id, run_id) REFERENCES runs(workspace_id, id),
    CHECK (jsonb_typeof(data) = 'object'),
    CHECK (data ?& ARRAY['summary','corrections','limitations'])
);
```

Immutable. Một run có tối đa một feedback; một submission có thể nhiều feedback qua các UUID retry mới. UI lấy mới nhất, lịch sử giữ tất cả. data giữ CorrectionData, không raw provider output. corrected_text do server áp dụng edits đã kiểm; danh sách corrections rỗng là hợp lệ.

### 2.11. learning_reports — ý học tập tự khai báo, không transcript

```sql
CREATE TABLE learning_reports (
    id uuid PRIMARY KEY,
    workspace_id uuid NOT NULL REFERENCES workspaces(id),
    period text NOT NULL CHECK (period IN ('day','week')),
    start_date date NOT NULL,
    end_date date NOT NULL,
    statement varchar(500) NOT NULL CHECK (length(btrim(statement)) > 0),
    origin text NOT NULL DEFAULT 'user_report' CHECK (origin = 'user_report'),
    source_run_id uuid NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (workspace_id, id),
    FOREIGN KEY (workspace_id, source_run_id) REFERENCES runs(workspace_id, id),
    CHECK ((period = 'day' AND end_date = start_date)
        OR (period = 'week' AND end_date = start_date + 6
            AND extract(isodow FROM start_date) = 1))
);
```

Immutable. source_run phải là chat.send. Tối đa 3 reports/run kiểm bằng service. Ngày mơ hồ không lưu report cho đến khi rõ; không cần thêm period=unknown. source_quote chỉ validate trong RAM, không có cột lưu.

### 2.12. learning_events — dấu vết thao tác ứng dụng

```sql
CREATE TABLE learning_events (
    id uuid PRIMARY KEY,
    workspace_id uuid NOT NULL REFERENCES workspaces(id),
    kind text NOT NULL CHECK (kind IN
        ('submission_saved','feedback_saved','activity_status_changed')),
    submission_id uuid,
    feedback_id uuid,
    activity_id uuid,
    entity_id uuid GENERATED ALWAYS AS (coalesce(submission_id, feedback_id, activity_id)) STORED,
    before_status text CHECK (before_status IN ('planned','completed','deferred')),
    after_status text CHECK (after_status IN ('planned','completed','deferred')),
    occurred_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (workspace_id, id),
    FOREIGN KEY (workspace_id, submission_id) REFERENCES submissions(workspace_id, id),
    FOREIGN KEY (workspace_id, feedback_id) REFERENCES feedback(workspace_id, id),
    FOREIGN KEY (workspace_id, activity_id) REFERENCES activities(workspace_id, id),
    CHECK (num_nonnulls(submission_id, feedback_id, activity_id) = 1),
    CHECK ((kind = 'submission_saved' AND submission_id IS NOT NULL
            AND before_status IS NULL AND after_status IS NULL)
        OR (kind = 'feedback_saved' AND feedback_id IS NOT NULL
            AND before_status IS NULL AND after_status IS NULL)
        OR (kind = 'activity_status_changed' AND activity_id IS NOT NULL
            AND after_status IS NOT NULL
            AND before_status IS DISTINCT FROM after_status))
);
```

Immutable. before_status=NULL chỉ khi tạo activity ban đầu; tạo với status=completed tạo một confirmation. Cập nhật không đổi status không tạo event. Chuyển sang completed lần nữa sau khi mở lại là một lượt mới, không phải số việc duy nhất. Typed columns là đề xuất để có FK thật; entity_id không được INSERT trực tiếp. [Generated columns](https://www.postgresql.org/docs/current/ddl-generated-columns.html).

### 2.13. journals — định danh kỳ và con trỏ bản hiện tại

```sql
CREATE TABLE journals (
    id uuid PRIMARY KEY,
    workspace_id uuid NOT NULL REFERENCES workspaces(id),
    period text NOT NULL CHECK (period IN ('day','week')),
    start_date date NOT NULL,
    end_date date NOT NULL,
    current_revision integer NOT NULL DEFAULT 1 CHECK (current_revision >= 1),
    UNIQUE (workspace_id, id),
    UNIQUE (workspace_id, period, start_date),
    CHECK ((period = 'day' AND end_date = start_date)
        OR (period = 'week' AND end_date = start_date + 6
            AND extract(isodow FROM start_date) = 1))
);
```

Chỉ current_revision được UPDATE; identity/kỳ bất biến. Không lưu status=current/stale: service tính khi đọc bằng signature hiện tại, không có cron đánh dấu.

### 2.14. journal_revisions — snapshot bất biến của từng bản tổng hợp

```sql
CREATE TABLE journal_revisions (
    journal_id uuid NOT NULL,
    revision integer NOT NULL CHECK (revision >= 1),
    workspace_id uuid NOT NULL REFERENCES workspaces(id),
    content jsonb NOT NULL,
    source_report_ids jsonb NOT NULL DEFAULT '[]'::jsonb,
    source_event_ids jsonb NOT NULL DEFAULT '[]'::jsonb,
    source_correction_ids jsonb NOT NULL DEFAULT '[]'::jsonb,
    source_signature text NOT NULL CHECK (source_signature ~ '^[0-9a-f]{64}$'),
    editor text NOT NULL CHECK (editor IN ('ai','user_correction')),
    updated_at timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (journal_id, revision),
    UNIQUE (workspace_id, journal_id, revision),
    FOREIGN KEY (workspace_id, journal_id) REFERENCES journals(workspace_id, id),
    CHECK (jsonb_typeof(content) = 'object'),
    CHECK (content ?& ARRAY['learner_summary','app_counts','limitations']),
    CHECK (jsonb_typeof(source_report_ids) = 'array' AND jsonb_array_length(source_report_ids) <= 500),
    CHECK (jsonb_typeof(source_event_ids) = 'array' AND jsonb_array_length(source_event_ids) <= 1000),
    CHECK (jsonb_typeof(source_correction_ids) = 'array' AND jsonb_array_length(source_correction_ids) <= 100)
);

ALTER TABLE journals ADD CONSTRAINT journals_current_revision_fk
    FOREIGN KEY (workspace_id, id, current_revision)
    REFERENCES journal_revisions(workspace_id, journal_id, revision)
    DEFERRABLE INITIALLY DEFERRED;
```

FK kiểm lúc COMMIT cho phép INSERT journal và revision 1 cùng transaction, nhưng không cho journal đã commit thiếu bản hiện tại. updated_at là lúc tạo snapshot, không đổi sau đó. Empty/event-only summary vẫn editor=ai theo contract; limitations ghi rõ không gọi model, không tuyên bố inference đã chạy. Không UNIQUE(source_signature): nguồn có thể quay lại nội dung cũ nhưng vẫn cần giữ chuỗi revision.

### 2.15. journal_corrections — yêu cầu đính chính có chủ đích

```sql
CREATE TABLE journal_corrections (
    id uuid PRIMARY KEY,
    workspace_id uuid NOT NULL REFERENCES workspaces(id),
    journal_id uuid NOT NULL,
    base_revision integer NOT NULL CHECK (base_revision >= 1),
    period text NOT NULL CHECK (period IN ('day','week')),
    start_date date NOT NULL,
    end_date date NOT NULL,
    instruction varchar(1000) NOT NULL CHECK (length(btrim(instruction)) > 0),
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (workspace_id, id),
    FOREIGN KEY (workspace_id, journal_id, base_revision)
        REFERENCES journal_revisions(workspace_id, journal_id, revision),
    CHECK ((period = 'day' AND end_date = start_date)
        OR (period = 'week' AND end_date = start_date + 6
            AND extract(isodow FROM start_date) = 1))
);
```

Immutable. Service sao chép kỳ từ journal, kiểm expected_revision trước/sau inference. Note cùng revision mới/receipt ghi một transaction. needs_clarification không INSERT note; câu hỏi trả về tạm, không cache trong DB.

### 2.16. history_index — mục lục artifacts, không sao chép nội dung

```sql
CREATE TABLE history_index (
    id bigint GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    workspace_id uuid NOT NULL REFERENCES workspaces(id),
    kind text NOT NULL CHECK (kind IN ('exercise','submission','feedback','journal')),
    exercise_id uuid,
    submission_id uuid,
    feedback_id uuid,
    journal_id uuid,
    journal_revision integer,
    entity_id uuid GENERATED ALWAYS AS
        (coalesce(exercise_id, submission_id, feedback_id, journal_id)) STORED,
    created_at timestamptz NOT NULL DEFAULT now(),
    FOREIGN KEY (workspace_id, exercise_id) REFERENCES exercises(workspace_id, id),
    FOREIGN KEY (workspace_id, submission_id) REFERENCES submissions(workspace_id, id),
    FOREIGN KEY (workspace_id, feedback_id) REFERENCES feedback(workspace_id, id),
    FOREIGN KEY (workspace_id, journal_id, journal_revision)
        REFERENCES journal_revisions(workspace_id, journal_id, revision),
    CHECK (num_nonnulls(exercise_id, submission_id, feedback_id, journal_id) = 1),
    CHECK ((kind = 'exercise' AND exercise_id IS NOT NULL AND journal_revision IS NULL)
        OR (kind = 'submission' AND submission_id IS NOT NULL AND journal_revision IS NULL)
        OR (kind = 'feedback' AND feedback_id IS NOT NULL AND journal_revision IS NULL)
        OR (kind = 'journal' AND journal_id IS NOT NULL AND journal_revision IS NOT NULL
            AND journal_revision >= 1))
);
```

Immutable. Một history item/journal revision. API adapter đọc đúng artifact; không thêm data JSON/transcript vào bảng. ID chỉ làm cursor, có thể có khoảng trống sau rollback; không phải số thứ tự hoàn tất thao tác.

## 3. Quan hệ và ánh xạ API

- Workspace 1→N materials, activities, exercises, submissions, feedback, reports, events, journals, requests và runs. MVP có tối đa một workspace, nhưng các khóa ngoại vẫn kiểm phạm vi.
- Catalog material 1→N material copies giữa các workspace; tối đa một copy/catalog/workspace. Template 1→N exercise snapshots. Hai danh mục là seed global, không chứa dữ liệu người học.
- Exercise 1→N submissions. Submission 0→N bản viết lại; cùng exercise. Submission 1→N feedback. Request 0→1 run; run 0→1 feedback hoặc 0→3 reports. Những run thất bại không có artifact thành công.
- Journal 1→N revisions, có đúng một current_revision tồn tại khi COMMIT. Correction tham chiếu đúng revision gốc của cùng journal/workspace; bản đính chính mới là revision kế tiếp.
- Events trỏ đúng một submission/feedback/activity; history trỏ đúng một exercise/submission/feedback/journal revision. Không FK kiểu “ID tùy ý trong bất kỳ bảng nào”.
- Mọi JOIN/UPDATE/SELECT của service phải dùng workspace_id từ session đã kiểm, không chỉ UUID client gửi. FK ghép bảo vệ liên kết ghi, không tự bảo vệ quyền đọc.
- `Workspace.goal` dựng từ goal_text/deadline; `Activity.data` dựng từ title/planned_period/planned_for/status theo contract đã đồng bộ. `Journal` ghép journal header + revision snapshot, tính status khi đọc. `HistoryItem.data` lấy từ đúng bảng/đúng revision, không dùng bản nhật ký hiện tại thay bản lịch sử.
- source-ID arrays và result_ids là liên kết logic do service kiểm. Không có FK tự động bên trong JSONB/UUID arrays; kiểm tồn tại, distinct, đúng workspace và đúng tool. Giữ arrays vì nguồn giới hạn theo SPEC và không có truy vấn reverse-source trong MVP; chuyển thành link tables khi thật sự cần FK từng nguồn/truy vấn ngược.

## 4. Bất biến và transaction contracts

### Validation bắt buộc ở service

- Validate JSON theo SPEC draft 2020-12, additionalProperties=false, enums, lengths, UUID/date formats; kiểm tất cả Unicode whitespace, không chỉ btrim. DB CHECK là lớp bổ sung, không thay JSON validator.
- learner_profile giữ đúng ba trường và enums hiện tại. Không tự gán trình độ/điểm. feedback.data và revision.content phải đúng CorrectionData/JournalContent, arrays không vượt giới hạn, counts không âm; không chấp nhận JSON chứa raw chat/prompt/error body.
- Material snapshot bằng dữ liệu đã đọc lúc tạo đề. Submission word_count được tính bằng regex SPEC; cha revision_of phải đã tồn tại trước INSERT, tránh chu kỳ do chèn nhiều bài liên kết lẫn nhau trong một transaction.
- Quote start/end dùng Unicode code points, end exclusive; substring khớp bài gốc; text edits không overlap. corrected_text được server tạo. Run operation phải đúng với artifact (feedback.generate cho feedback, chat.send cho reports).
- Có report ngày rõ mới INSERT; tuần chuẩn hóa thứ Hai–Chủ nhật, không tự chia cho ngày. Không lưu việc dự định hoặc kỳ bắt đầu trong tương lai như việc đã học.
- Correction period/start/end phải bằng header journal; base_revision phải là current_revision đã kiểm. Cung cấp mọi notes liên quan theo `(created_at,id)`, mới hơn ưu tiên khi cùng nội dung; chưa có khóa nội dung để DB tự quyết định notes nào tương đương.
- source_*_ids là toàn bộ nguồn cung cấp cho tổng hợp, không chỉ used_*_ids model nêu. Không nguồn quá giới hạn bị âm thầm bỏ; quá 500/1000/100 → CONTEXT_LIMIT, không commit bản mới.
- error_code thuộc Error enum của SPEC, đã gồm INTERNAL_ERROR theo OpenAPI đề xuất. INTERNAL_ERROR sau claim kết thúc receipt HTTP 500/run failed khi DB khỏe; nếu success đã commit không ghi đè. metadata/response được serialize theo allowlist; không ghi request body, messages, source_quote, provider reply hoặc nội dung lỗi tự do vào requests/runs/log. 400/405/413/415 không persist; DB không khỏe/không rõ commit trả DATABASE_UNAVAILABLE và replay cùng key sau phục hồi.

### Khóa và lưu nguyên tử

**Đề xuất:** READ COMMITTED với khóa hàng ngắn, thay vì transaction dài hoặc SERIALIZABLE toàn ứng dụng. Khóa tránh writer làm nguồn thay đổi giữa bước đọc lại/commit; không cần source_version mới. Cách dùng khóa và mức cô lập tham chiếu [Explicit Locking](https://www.postgresql.org/docs/current/explicit-locking.html) và [Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html).

1. Mọi transaction ghi artifact/source/metadata mutable lấy `SELECT id FROM workspaces WHERE id=:workspace_id FOR UPDATE` trước. Thứ tự khóa cố định: workspace → journal (nếu có) → run → request. Các thao tác đọc thường không khóa. Khóa này chỉ giữ trong các pha DB ngắn, tuyệt đối không qua HTTP/model.
2. Thao tác không-model: khóa workspace, claim receipt, kiểm hash/version/quota, ghi artifact + event/history nếu có, hoàn tất receipt, COMMIT cùng nhau. Workspace version chỉ tăng khi profile/goal/context/material/activity thay đổi; chọn lại catalog không đổi dữ liệu thì không tăng.
3. Thao tác model: transaction đầu khóa workspace, claim receipt, kiểm target/version, tạo run bằng cùng request UUID, lấy context/source snapshot rồi COMMIT. Insert run bị unique running conflict → hoàn tất receipt RUN_BUSY trong transaction sau rollback savepoint; không gọi model.
4. Inference chạy ngoài transaction. Khi commit: khóa workspace → journal → run → request; kiểm run vẫn running và chưa hết deadline, rồi kiểm lại journal revision/signature nếu liên quan. Thành công ghi artifact/event/history, run succeeded và receipt 200 trong cùng COMMIT. Một late result sau terminal state bị bỏ.
5. **Mọi report/event/correction writer đều phải khóa cùng hàng workspace trước INSERT.** Nhờ vậy snapshot và commit-time scan dùng nguồn nhất quán trong pha ngắn. Chỉ thêm khóa ở summarizer mà bỏ source writers không đủ bảo vệ.
6. Journal mới: INSERT header + revision 1 + history trong một transaction. Bản mới: expected_revision phải còn đúng, INSERT revision=current+1, UPDATE pointer, INSERT history. Correction: INSERT note, tính lại signature bao gồm note mới, INSERT revision/pointer/history cùng receipt; nếu có xung đột/clarification thì không note hoặc revision nửa chừng.
7. Same request/hash terminal → replay receipt; same ID khác hash → IDEMPOTENCY_CONFLICT; đang chạy → RUN_BUSY. Không UPDATE payload_hash hoặc mở lại request đã completed. Retry chủ động dùng UUID mới. Non-model branches của journal có receipt nhưng không run.
8. Startup của single worker, trước nhận request: khóa workspace, chuyển mọi run running thành interrupted/INTERRUPTED và hoàn tất receipt tương ứng. Hoàn tất cả receipt in_progress còn lại bằng INTERRUPTED; không gọi lại model. Nếu DB không khỏe thì chưa nhận request ghi. Không dùng cơ chế này với nhiều worker.

### Signature và counts

Canonical nguồn đề xuất là JSON UTF-8, sort keys, separators không khoảng trắng, không normalize nội dung; UUID lower-case, dates ISO, time UTC ISO. Gồm kỳ + sorted report objects `(id,period,start_date,end_date,statement,origin)` + sorted event objects `(id,kind,entity_id,before_status,after_status,occurred_at)` + sorted correction objects `(id,journal_id,base_revision,period,start_date,end_date,instruction,created_at)`. Sort các arrays theo UUID trước khi SHA-256. Không đưa `now`, thời điểm mở trang, request ID, run ID hoặc nội dung summary vào hash. Cùng nguồn phải cùng signature dù mở lại lúc khác.

Reports/corrections chọn theo ngày nghiệp vụ, không created_at. Events chọn theo `[00:00 ngày đầu, 00:00 ngày sau ngày cuối)` tại Asia/Ho_Chi_Minh, đổi sang timestamptz. Kỳ đang diễn ra chỉ phản ánh nguồn đã commit lúc snapshot; không giả định cả ngày/tuần đã kết thúc.

Counts: mỗi submission_saved = 1 submitted_drafts; mỗi feedback_saved = 1 feedback_results; activity_status_changed có after_status=completed = 1 completion_confirmations. Idempotent replay không tăng counts. Counts là lượt thao tác, không số việc duy nhất, giờ học hoặc tiến bộ; sửa lời khai không sửa events.

## 5. Indexes và truy vấn phục vụ

Không thêm GIN/full-text/partitioning khi MVP chưa có truy vấn nội dung. PK/UNIQUE tự có B-tree; FK không tự tạo index ở phía tham chiếu. Các index dưới đây là đề xuất, cần EXPLAIN trên fixture khi triển khai; không khẳng định planner luôn chọn index. [Constraints](https://www.postgresql.org/docs/current/ddl-constraints.html), [CREATE INDEX](https://www.postgresql.org/docs/current/sql-createindex.html).

```sql
CREATE INDEX materials_recent_idx ON materials(workspace_id, created_at DESC, id DESC);
CREATE INDEX activities_recent_idx ON activities(workspace_id, updated_at DESC, id DESC);
CREATE INDEX feedback_by_submission_idx ON feedback(workspace_id, submission_id, created_at DESC, id DESC);
CREATE INDEX submission_rewrites_idx ON submissions(workspace_id, revision_of, created_at, id)
    WHERE revision_of IS NOT NULL;
CREATE INDEX reports_period_idx ON learning_reports(workspace_id, period, start_date, id);
CREATE INDEX events_period_idx ON learning_events(workspace_id, occurred_at, id);
CREATE INDEX corrections_period_idx ON journal_corrections(workspace_id, period, start_date, created_at, id);
CREATE INDEX journal_revisions_recent_idx ON journal_revisions(workspace_id, updated_at DESC, journal_id, revision DESC);
CREATE INDEX history_page_idx ON history_index(workspace_id, id DESC);
CREATE UNIQUE INDEX history_artifact_once_idx ON history_index(workspace_id, kind, entity_id)
    WHERE kind <> 'journal';
CREATE UNIQUE INDEX history_revision_once_idx ON history_index(workspace_id, journal_id, journal_revision)
    WHERE kind = 'journal';
CREATE UNIQUE INDEX event_submission_once_idx ON learning_events(workspace_id, submission_id)
    WHERE submission_id IS NOT NULL;
CREATE UNIQUE INDEX event_feedback_once_idx ON learning_events(workspace_id, feedback_id)
    WHERE feedback_id IS NOT NULL;
CREATE UNIQUE INDEX one_running_run_per_workspace_idx ON runs(workspace_id)
    WHERE status = 'running';
```

- materials_recent_idx: Q01, danh sách tài liệu mới nhất, tối đa 50.
- activities_recent_idx: Q01, 20 việc mới cập nhật; không phải index cho dashboard tiến độ.
- feedback_by_submission_idx: Q03, bản sửa mới nhất/tất cả bản sửa của bài.
- submission_rewrites_idx: Q04, các bản viết lại trực tiếp của bài.
- reports_period_idx: Q07, reports ngày hoặc tuần trong kỳ; không tải transcript.
- events_period_idx: Q07/Q08, nguồn theo timestamp range và counts.
- corrections_period_idx: Q07, notes theo kỳ; merge-sort bằng created_at,id ở service cho day+week.
- journal_revisions_recent_idx: Q01, 10 journals có current revision cập nhật gần nhất; join pointer loại bản cũ.
- history_page_idx: Q05, cursor ID giảm dần; không OFFSET hoặc timestamp cursor.
- history_artifact_once_idx/history_revision_once_idx: INSERT history cùng artifact/revision, tránh history trùng khi replay Q09.
- event_submission_once_idx/event_feedback_once_idx: INSERT đúng một event/artifact, giữ Q08 không đếm trùng.
- one_running_run_per_workspace_idx: Q10/INSERT run, DB chặn run thứ hai và tìm run cần phục hồi.
- requests PK `(workspace_id,request_id)`: Q09 claim/replay. UNIQUE thêm tool cho FK run→đúng receipt; không thêm index riêng payload_hash.
- journals UNIQUE `(workspace_id,period,start_date)`: Q06 lookup kỳ. Revisions PK/scoped UNIQUE: Q06 và FK pointer/correction/history; đọc bản cụ thể không cần index signature.
- UUID PK của workspaces/artifacts: Q01/Q03/Q04 và batch hydration Q05. Các UNIQUE `(workspace_id,id)`/submission triple bảo vệ FK scoped; không tạo thêm cùng index với tên khác.
- catalog/template PK: tìm seed theo UUID trong workspace.read/exercise.create; 100/20 rows nên list đọc tuần tự. Không thêm FK-side indexes khác cho purge vì MVP không có purge; xem lại khi có deletion hoặc kế hoạch query chứng minh cần.

## 6. Top 10 mẫu truy vấn cần phục vụ

Đây là 10 mục đích truy vấn chính; Q01/Q07/Q09 có vài SQL statements cho cùng một operation. `:name` là bind parameter của SQLAlchemy, không ghép chuỗi SQL từ input. Mọi ID đã validate UUID; ngày kỳ đã chuẩn hóa. Mutation statements nằm trong transaction contract ở mục 4.

### Q01 — Mở workspace, đọc profile và danh sách khi model tắt

```sql
SELECT * FROM workspaces WHERE id = :workspace_id;
SELECT * FROM materials WHERE workspace_id = :workspace_id ORDER BY created_at DESC, id DESC LIMIT 50;
SELECT * FROM activities WHERE workspace_id = :workspace_id ORDER BY updated_at DESC, id DESC LIMIT 20;
SELECT j.*, r.* FROM journals j
JOIN journal_revisions r ON r.workspace_id=j.workspace_id AND r.journal_id=j.id AND r.revision=j.current_revision
WHERE j.workspace_id=:workspace_id ORDER BY r.updated_at DESC, j.id DESC LIMIT 10;
```

Đọc thêm catalog/template seed bằng SELECT, không model. Serializer dùng explicit columns/aliases thay SELECT * khi dựng API để tránh trùng tên; projections minh họa không phải response JSON.

### Q02 — Lưu hồ sơ bằng optimistic version check

```sql
UPDATE workspaces SET goal_text=:goal_text, deadline=:deadline,
    study_context=:study_context, learner_profile=:learner_profile,
    version=version+1, updated_at=now()
WHERE id=:workspace_id AND version=:expected_version
RETURNING *;
```

0 rows → VERSION_CONFLICT sau kiểm workspace tồn tại. material/activity save cũng tăng version theo expected_version trong cùng transaction; không AI tự gọi mutation này.

### Q03 — Đọc đúng bài, đề/snapshot và bản sửa mới nhất

```sql
SELECT s.*, e.prompt, e.material_snapshot, f.id AS feedback_id,
       f.data, f.corrected_text, f.created_at AS feedback_created_at
FROM submissions s JOIN exercises e ON e.workspace_id=s.workspace_id AND e.id=s.exercise_id
LEFT JOIN LATERAL (
    SELECT * FROM feedback
    WHERE workspace_id=s.workspace_id AND submission_id=s.id
    ORDER BY created_at DESC, id DESC LIMIT 1
) f ON true
WHERE s.workspace_id=:workspace_id AND s.id=:submission_id;
```

Không feedback vẫn trả bài để retry. Khi UI chọn feedback ID cụ thể, đọc chính ID đó bằng scoped PK/UNIQUE; không tự đổi sang bản mới nhất.

### Q04 — Tìm các bản viết lại trực tiếp, giữ bài cha

```sql
SELECT id, exercise_id, revision_of, text, word_count, created_at
FROM submissions WHERE workspace_id=:workspace_id AND revision_of=:parent_submission_id
ORDER BY created_at, id;
```

Không cần recursive tree UI trong MVP. Bài cha đọc bằng Q03.

### Q05 — Trang lịch sử dùng cursor, hydrate đúng artifact/revision

```sql
SELECT id, kind, entity_id, journal_revision, created_at
FROM history_index WHERE workspace_id=:workspace_id AND id < :before_id
ORDER BY id DESC LIMIT :fetch_limit;
```

Trang đầu bỏ điều kiện id<before_id; fetch_limit=limit+1 với limit 1..50 theo SPEC. Hydrate theo kind bằng batch scoped queries; journal dùng đúng `(journal_id,journal_revision)`. next_before_id là ID item cuối trả nếu còn trang. Các mục mới xuất hiện sau khi mở trang cần refresh trang đầu; pagination không hứa snapshot liên tục qua nhiều HTTP requests.

### Q06 — Đọc journal hiện tại hoặc bản lịch sử của đúng kỳ

```sql
SELECT j.id, j.period, j.start_date, j.end_date, r.*
FROM journals j JOIN journal_revisions r
  ON r.workspace_id=j.workspace_id AND r.journal_id=j.id AND r.revision=j.current_revision
WHERE j.workspace_id=:workspace_id AND j.period=:period AND j.start_date=:start_date;
```

Bản lịch sử: tra revisions với workspace_id/journal_id/revision cụ thể. Tính current/stale bằng Q07+signature; model tắt vẫn trả bản đã lưu cùng status, không bắt inference.

### Q07 — Lấy trọn nguồn đúng kỳ cho tổng hợp/đính chính

```sql
SELECT * FROM learning_reports WHERE workspace_id=:workspace_id AND (
    (period='day' AND start_date BETWEEN :start_date AND :end_date)
    OR (:period='week' AND period='week' AND start_date=:start_date))
ORDER BY id LIMIT 501;

SELECT * FROM learning_events WHERE workspace_id=:workspace_id
    AND occurred_at>=:start_instant AND occurred_at<:end_exclusive_instant
ORDER BY occurred_at, id LIMIT 1001;

SELECT * FROM journal_corrections WHERE workspace_id=:workspace_id AND (
    (period='day' AND start_date BETWEEN :start_date AND :end_date)
    OR (:period='week' AND period='week' AND start_date=:start_date))
ORDER BY created_at, id LIMIT 101;
```

Ngày có start=end nên không lấy nguồn cả tuần. Giới hạn +1 để phát hiện vượt và từ chối, không tổng hợp phần bị cắt. 3 scans trong transaction giữ khóa workspace; không scan qua thời gian inference. Truy vấn có OR dùng prefix workspace/index hoặc bitmap tùy planner; chỉ đổi thành UNION ALL nếu EXPLAIN cho thấy cần.

### Q08 — Đếm hoạt động ứng dụng bằng SQL, độc lập lời khai/model

```sql
SELECT count(*) FILTER (WHERE kind='submission_saved') AS submitted_drafts,
       count(*) FILTER (WHERE kind='feedback_saved') AS feedback_results,
       count(*) FILTER (WHERE kind='activity_status_changed' AND after_status='completed') AS completion_confirmations
FROM learning_events WHERE workspace_id=:workspace_id
    AND occurred_at>=:start_instant AND occurred_at<:end_exclusive_instant;
```

Đọc cùng snapshot nguồn Q07; không lấy trạng thái hiện tại của activities để viết lại số lượt quá khứ.

### Q09 — Claim/replay request, giữ một effect

```sql
INSERT INTO requests(workspace_id,request_id,tool,payload_hash)
VALUES (:workspace_id,:request_id,:tool,:payload_hash)
ON CONFLICT (workspace_id,request_id) DO NOTHING RETURNING request_id;
SELECT * FROM requests WHERE workspace_id=:workspace_id AND request_id=:request_id;
```

Không INSERT được thì so hash/state và replay/error; không ON CONFLICT DO UPDATE ghi đè hash. Chat receipt thành công nhưng RAM reply hết → RESULT_EXPIRED, giữ reports cũ. Journal non-inference cũng đi đường này, không tra run rồi suy ra cần retry.

### Q10 — Tra run và phục hồi lượt bị ngắt

```sql
SELECT * FROM runs WHERE workspace_id=:workspace_id AND id=:run_id;
UPDATE runs SET status='interrupted', error_code='INTERRUPTED', finished_at=now()
WHERE workspace_id=:workspace_id AND status='running' RETURNING id;
UPDATE requests SET state='completed', http_status=409, error_code='INTERRUPTED',
    error_retryable=true, response_json=NULL, result_ids='{}'::uuid[], completed_at=now()
WHERE workspace_id=:workspace_id AND state='in_progress';
```

Hai UPDATE chỉ chạy lúc startup single worker trong transaction đã khóa workspace, trước nhận traffic. INSERT run dùng unique running index để claim quyền; không SELECT-check rồi INSERT không ràng buộc. run.read không tự tiếp tục inference.

## 7. Soft-delete, audit và retention

**Không thêm soft-delete trong MVP:** PRD/ADR chưa có xóa/ẩn/restore UI; không thêm deleted_at giả dùng. Tài liệu, bài, feedback, reports, notes và revisions giữ lâu dài theo SPEC A10 cho đến khi owner xử lý DB. Không cascade delete hoặc background purge. Retention/xóa/export có dữ liệu thật: `TODO(project owner)` cho giai đoạn sau, không chặn MVP.

Audit phục vụ yêu cầu hiện tại: workspace version/timestamps cho thay đổi hồ sơ; compact events giữ chuyển status và thời điểm lưu bài/kết quả; requests giữ hash/kết quả idempotent; runs giữ model/prompt_version/attempts/errors/timing; revisions và correction notes giữ bản trước/nguồn. Không có full before/after history cho mọi lần sửa goal/material; đây không phải audit đầy đủ từng giá trị cũ. Không thêm audit_log chứa bản sao chat hoặc content mọi thao tác.

Chat/reply/source_quote/raw prompt chỉ RAM; response cache ≤10 phút/restart. Metadata logs ≤30 ngày, ngoài các bảng này. DB requests/runs giữ metadata lâu dài vì xóa receipt sẽ cho phép request ID cũ tạo effect mới; muốn purge metadata phải định nghĩa lại thời hạn idempotency và giữ tombstone trước. Kể cả backup DB cũng không được chứa transcript; backup có thể còn artifacts cũ đến khi owner xác định lịch retention backup.

**Bảo vệ bất biến đề xuất:** migration owner khác runtime role `studycraft_app`; runtime không sở hữu bảng, không superuser/DDL/TRUNCATE/DELETE và không được hưởng quyền đó qua role khác/PUBLIC. DB role không thay permission checks theo mode UI; model không có DB connection. Quyền cột/bảng theo [PostgreSQL GRANT](https://www.postgresql.org/docs/current/sql-grant.html).

```sql
-- Roles/schema privileges are provisioned separately by the migration owner.
GRANT SELECT ON ALL TABLES IN SCHEMA public TO studycraft_app;
GRANT INSERT ON materials, activities, requests, runs, exercises, submissions,
    feedback, learning_reports, learning_events, journals, journal_revisions,
    journal_corrections, history_index TO studycraft_app;
GRANT UPDATE (goal_text, deadline, study_context, learner_profile, version, updated_at)
    ON workspaces TO studycraft_app;
GRANT UPDATE (catalog_id, title, description, content, updated_at) ON materials TO studycraft_app;
GRANT UPDATE (title, planned_period, planned_for, status, updated_at) ON activities TO studycraft_app;
GRANT UPDATE (current_revision) ON journals TO studycraft_app;
GRANT UPDATE (state, http_status, error_code, error_retryable, response_json, result_ids, completed_at)
    ON requests TO studycraft_app;
GRANT UPDATE (status, model, attempts, input_tokens, output_tokens, context_truncated,
    context_metadata, error_code, result_ids, finished_at) ON runs TO studycraft_app;
GRANT USAGE, SELECT ON SEQUENCE history_index_id_seq TO studycraft_app;
```

Workspace và seed được owner tạo lúc bootstrap; không public tool tạo workspace. Runtime không được UPDATE/DELETE exercise/submission/feedback/report/event/revision/note/history. SELECT grants chỉ áp dụng các bảng đã tạo, kiểm lại grants trong migration mới; không dùng owner credential trong app. FK không chặn owner/superuser sửa dữ liệu trực tiếp.

Khi có deletion yêu cầu thật: chọn archive tài liệu/việc mutable hay purge cả nguồn học; giữ khả năng đọc snapshot và điều chỉnh FK, history, source signatures, receipts và backup cùng policy. Không chỉ thêm deleted_at rồi bỏ nguồn khỏi nhật ký cũ.

## 8. Multi-tenancy — phạm vi dữ liệu người dùng

Chưa có nhiều người dùng trong MVP. workspace_id là phạm vi dữ liệu/ngữ cảnh, không phải cơ chế auth hay tenant isolation đã triển khai. FK ghép chống tham chiếu sai workspace; service luôn dùng ID từ session/instance config đã kiểm. Catalog/template global chỉ chứa seed public.

Không thêm tenant_id, user_id, membership hoặc RLS khi chưa có SaaS. Chuyển multi-user cần owner/auth/membership, bỏ UNIQUE(subject), xác định catalog visibility, kiểm RLS/quyền service và migration IDs/FKs trước mở mạng. Không lấy một workspace ID do client tự nhập làm quyền truy cập.

## 9. Quyết định khó đổi về sau

- **Bất biến và liên kết bản viết lại:** chọn append-only + revision_of, thay vì overwrite; giữ bài gốc nhưng cần migration chuỗi/IDs nếu đổi mô hình.
- **UUID global và runs.id=request_id:** chọn hợp đồng SPEC, thay vì ID riêng/run; request IDs phải UUID duy nhất do client sinh, cross-workspace collision bị PK chặn. Đổi sang ID run riêng ảnh hưởng retry/run.read/FKs.
- **Một workspace english/short_writing:** chọn UNIQUE subject và CHECK, thay vì multi-user/multi-subject sẵn; đơn giản MVP nhưng phải sửa ownership/constraints/API trước mở rộng.
- **Chat không lưu:** chọn RAM + reports ngắn, thay vì transcript; không thể khôi phục câu gốc hoặc đánh giá lại mọi hội thoại sau này. Bật lưu mới cần quyết định retention mới, không có dữ liệu quá khứ để backfill.
- **Snapshot đề/tài liệu:** chọn lưu bản sao tại exercise, thay vì JOIN tài liệu hiện tại; tốn dung lượng nhưng giữ nguồn cũ. Mẫu seed sửa không cập nhật bài đã tạo.
- **JSONB payload/nguồn:** chọn cấu trúc hợp đồng bounded, thay vì chuẩn hóa từng correction/source; ít bảng nhưng FK nguồn/JSON schema cần service. Chuyển link tables cần backfill/check mọi revision.
- **Canonical signature và timezone/tuần:** chọn A05 + thuật toán mục 4, thay vì timezone người dùng tùy chỉnh; đổi làm cache/kỳ nguồn khác, cần signature-version/migration trước đổi.
- **Cursor history bằng bigint:** chọn SPEC id cursor, thay vì timestamp; giữ gaps và thứ tự cấp ID. Đổi cursor ảnh hưởng frontend và pagination; client không giả ID liên tục.
- **Typed references events/history:** chọn FK thật + entity_id sinh tự động, thay vì polymorphic UUID không FK; thêm artifact kind cần columns/CHECK/index/serializer/diagram cùng migration.
- **Quota/word limits/rubric:** chọn giả định SPEC 1–300 từ, correction-v2 và quotas, thay vì hard-code điểm thi; đổi cần cập nhật contracts/constraints/validators, không gán rubric mới cho feedback cũ.
- **Không purge receipts:** chọn effect-once lâu dài, thay vì xóa metadata sau 30 ngày như logs; metadata tăng nhưng retry UUID cũ vẫn an toàn. Purge cần policy tombstones/expiry được chốt.
- **Chỉ audit theo mục đích:** chọn events/versions/receipts, thay vì full event sourcing; ít dữ liệu nhưng không tái dựng mọi giá trị goal/material trước đây.

planned_period đã đồng bộ giữa SPEC/OpenAPI/schema ở P01; cần kiểm default, hash và ngày đầu tuần khi triển khai US-003. Nếu đổi multi-user, retention, signature hoặc kiểu liên kết nguồn, cập nhật ADR 002/005 hoặc tạo ADR kế tiếp với Status phù hợp; không đánh dấu Accepted chỉ vì có tài liệu này.

## 10. Sơ đồ và kiểm chứng bàn giao

Sơ đồ ER — quan hệ thực thể: [docs/diagrams/database-er.mmd](../diagrams/database-er.mmd). Sơ đồ chỉ vẽ FK thật; nét đứt là quan hệ không định danh theo ký hiệu ER, không có nghĩa thiếu FK. Source-ID arrays/result_ids là liên kết logic được ghi trong comments, không vẽ như FK. Constraint/DDL ở trên là nguồn chi tiết, diagram không thay validator.

Khi triển khai migration, kiểm với PostgreSQL database test riêng:

1. Tạo đủ 16 bảng/index/grants, seed một workspace, chạy Q01–Q10 với fixtures; rollback/drop DB test không đụng DB thật.
2. FK từ bài/feedback/history/correction sang workspace hoặc exercise sai phải fail; header journal commit thiếu current revision phải fail.
3. App role UPDATE/DELETE bài gốc/feedback/revisions phải bị từ chối. Bản viết lại thêm bài mới; history bản cũ đọc đúng revision.
4. Hai request cùng UUID/input chỉ một artifact/event/history; khác input conflict; hai model UUID đồng thời chỉ một running; terminal retry cùng UUID không inference.
5. Source đổi trong lúc inference → VERSION_CONFLICT và không artifact/note nửa chừng; correction ngày vào tuần, correction tuần không vào ngày; cùng nguồn không revision/model mới.
6. Empty/event-only journal có receipt không run; chat restart/expiry không nhân report. Canary text trong chat thường không xuất hiện trong DB/receipt/log/backup; không kiểm canary nằm trong report/explicit correction đã cho phép giữ.
7. Biên midnight/thứ Hai/timezone, completed→completed, deferred→completed, tạo completed và replay cho đúng counts. Trên source quota +1 phải từ chối thay vì cắt.
8. EXPLAIN (ANALYZE, BUFFERS) các SELECT trên fixture 10.000 history entries trong DB test; kiểm target NFR-L01 khi có app. Không ép tiny seed tables dùng index, không chạy EXPLAIN ANALYZE mutation lên dữ liệu thật.

**Mức kiểm chứng tài liệu:** kiểm đối chiếu stories/SPEC, tên bảng/quan hệ/links và nội dung SQL; chưa chứng minh DDL chạy, index plan/latency, quyền runtime hoặc render Mermaid. Không có migration hay thay đổi database thật trong yêu cầu thiết kế này.
