# StudyCraft — Thiết kế kiến trúc MVP

**Trạng thái: Proposed — đề xuất, 2026-10-07.** Nguồn: [PRD](../requirements/prd.md), [18 user stories](../requirements/user-stories.md), [SPEC v2](../SPEC.md). Repo hiện có tài liệu, chưa có ứng dụng để kiểm chứng thiết kế.

Thiết kế phục vụ một người học trên máy cá nhân, bắt đầu bằng sửa bài viết tiếng Anh. Nghe/nói/đọc là tầm nhìn dài hạn. Thông tin nhóm hai người trong mẫu giới thiệu khác PRD làm solo; khác biệt đó không thay yêu cầu một người dùng local.

**Nguồn quyết định:** PostgreSQL, model local trước, chat riêng và nhật ký tóm tắt đã được người dùng chọn. Jinja, LM Studio, giới hạn dữ liệu và mọi NFR mới dưới đây vẫn là đề xuất. Chưa chọn phiên bản Qwen hoặc cấu hình máy; không tự dùng API cloud hoặc fine-tuning.

## 1. Thành phần và trách nhiệm

**Monolith — một ứng dụng backend chia theo trách nhiệm**, không phải các dịch vụ triển khai riêng. Có ba tiến trình chính trên cùng máy: ứng dụng, PostgreSQL và runtime model.

- **Trình duyệt:** các khu vực Tài liệu, Luyện viết/Kết quả, Chat, Nhật ký. Jinja + HTML/CSS/JavaScript thuần; lấy JSON bằng fetch. Chat tạm trong RAM của tab. Không tự gửi câu hỏi sau sửa bài.
- **Web/API FastAPI:** phục vụ `/`, `/static/*`, `/health`; transport đề xuất mới trong [OpenAPI](../api/openapi.json) dùng `/api/v1`, GET cho ba tool đọc và POST `/api/v1/tools/{name}` cho chín tool ghi, thay bố trí toàn-POST `/api/tools/{name}` trước đó. Kiểm Host/Origin/session/CSRF, giới hạn body, schema đầu vào và Problem HTTP; giữ tool allowlist và bất biến nghiệp vụ SPEC.
- **Nghiệp vụ hồ sơ và bài:** hồ sơ/mục tiêu, tài liệu, hoạt động, đề mẫu/đề riêng, nộp bài, bản viết lại và lịch sử. Lưu submission trước model; giữ material snapshot của đề cũ. Phục vụ US-001, US-002, US-003, US-004, US-005, US-006, US-010, US-011.
- **Nghiệp vụ AI:** sửa bài và xử lý lỗi (US-007, US-008, US-009); hỏi đáp/trích khai báo (US-012, US-013); tóm tắt/đính chính nhật ký (US-014, US-015, US-016). Nhật ký đếm app events bằng code; model chỉ tổng hợp phần lời khai/đính chính.
- **Runner giới hạn:** chạy đúng mode do thao tác UI chọn: feedback.generate, chat.send, journal.summarize hoặc journal.correct. Đọc snapshot → tạo context → gọi model → kiểm tra → lưu. Không planning tự do, chuỗi agent hoặc model tự chọn tool. Tối đa một run running/workspace.
- **Context + validators:** lấy đúng đề/bài/tài liệu hoặc đúng kỳ nhật ký; kiểm JSON, nguồn trích dẫn, offsets và phiên bản. Ghép các text edits hợp lệ từ cuối bài về đầu, giữ bài gốc. Nội dung model không có quyền đổi mục tiêu/trạng thái. Phục vụ US-008, US-018.
- **Persistence — lớp truy cập dữ liệu:** PostgreSQL, SQLAlchemy async + psycopg và Alembic là bộ thư viện đề xuất. Transaction ngắn; mỗi request/pha transaction có session riêng, không giữ kết nối qua thời gian chờ model hoặc chia sẻ session giữa request. Theo [SQLAlchemy async](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html).
- **RAM cache + log metadata:** cache reply chat tạm; request/run IDs và các kết quả durable được tra trong database. Log mode, mã lỗi, thời gian và entity IDs; không log body/prompt/reply. Phục vụ US-017 và chẩn đoán các story khác.

Các tên module `app/routes.py`, `tools.py`, `runner.py`, `context.py`, `journals.py`, `db.py`, `local_model.py` tham chiếu cấu trúc dự kiến trong SPEC; chưa tồn tại trong repo. Không thêm repository framework hoặc event bus.

**Dữ liệu:** dùng các bảng SPEC mục 9: workspace/material/activity, exercise/submission/feedback, learning_report/event, journal/revision/correction, request/run/history_index. Bài gốc và phản hồi bất biến; bản viết lại có revision_of. Đính chính và journal revision mới cùng transaction; giữ bản trước.

Schema PostgreSQL chi tiết, các khoảng trống hợp đồng và truy vấn cần phục vụ: [database-schema.md](database-schema.md); sơ đồ quan hệ: [database-er.mmd](../diagrams/database-er.mmd). Cả hai là đề xuất thiết kế, chưa có migration đã chạy.

## 2. Giao tiếp và các luồng

### Giao thức và sync/async

- **Browser ↔ ứng dụng:** HTTP cùng origin, HTML/CSS/JS cho trang; JSON cho tool API. Một request chờ một kết quả hoặc lỗi cuối cùng — sync theo góc nhìn người dùng. Không HTTP 202/job queue, WebSocket hoặc streaming trong MVP.
- **Bên trong ứng dụng:** gọi hàm trực tiếp. Dùng async/await — nhường xử lý lúc chờ I/O — cho HTTP model và truy cập DB, để thao tác đọc/lưu không phải chờ inference kết thúc. Không chạy model CPU trong process FastAPI. Cách dùng await theo [FastAPI async](https://fastapi.tiangolo.com/async/).
- **Ứng dụng ↔ PostgreSQL:** giao thức PostgreSQL qua TCP loopback, cổng tham chiếu 5432. Pool đề xuất 5 kết nối, không overflow; query có tham số.
- **Ứng dụng ↔ runtime:** HTTP/JSON loopback, base URL đề xuất `http://127.0.0.1:1234/v1`, POST `/chat/completions`, stream=false. Adapter đọc `choices[0].message.content`; luôn kiểm JSON phía app. Giao thức tham chiếu [LM Studio Chat Completions](https://lmstudio.ai/docs/developer/openai-compat/chat-completions).
- **Database → UI:** đọc khi người học mở lịch sử/nhật ký. Không scheduler, không tác vụ nền phải sống qua restart. GET `/health` chỉ kiểm ứng dụng/DB, không inference; model lỗi không làm core data phụ thuộc vào model.

### Nộp và sửa bài

1. submission.add lưu bài + event/history + receipt request trong một transaction; trả ID. Đây là request riêng, hoàn tất trước feedback.generate.
2. feedback.generate kiểm request ID, bài/workspace và giành quyền run bằng unique constraint; lấy snapshot rồi đóng transaction.
3. Runner gọi local adapter với context có giới hạn. Model không được gọi SQL, HTTP, shell hoặc filesystem.
4. Validator kiểm schema, quotes và text edits. Transaction mới lưu feedback/event/history và kết thúc run/request, chỉ khi run còn hợp lệ.
5. UI hiển thị kết quả ở panel sửa bài. Timeout/lỗi giữ bài gốc; không tạo reply chat.

### Chat và nhật ký

Chat chỉ trích khai báo đã học từ tin hiện tại; source_quote kiểm trong RAM rồi bỏ. Lưu learning_reports ngắn, reply ở RAM; không lưu transcript.

Khi mở kỳ nhật ký theo giả định hiện tại: lấy reports/events/correction notes, tính source_signature. Cùng nguồn trả bản cũ; kỳ trống hoặc chỉ có app events tính bằng code, không gọi model. Nguồn thay đổi mới inference; trước commit kiểm lại signature và revision. Đính chính dùng journal_id/expected_revision, không đổi app counts; mơ hồ yêu cầu làm rõ và giữ bản trước.

### Lặp request, hủy và khôi phục

- Unique `(workspace_id, request_id)` cùng payload hash: cùng ID/cùng input trả kết quả cũ; khác input → IDEMPOTENCY_CONFLICT. Partial unique run running/workspace chặn run model thứ hai bằng RUN_BUSY. [PostgreSQL constraints](https://www.postgresql.org/docs/current/ddl-constraints.html) là cơ chế DB, không khóa RAM thay thế.
- Same ID đang chạy không gọi model lần nữa. Run failed/interrupted không tự chạy lại; người học retry chủ động bằng UUID mới. Mất response: kiểm run.read hoặc replay request cũ trước khi quyết định retry.
- Nhánh nhật ký không inference có receipt/artifact nhưng không run; run.read NOT_FOUND không đủ để suy ra cần gửi UUID mới.
- Startup của single worker đánh dấu run còn running thành interrupted và hoàn tất receipt tương ứng; không tự tiếp tục inference hoặc tái tạo chat.
- Hủy handler nếu xảy ra: rollback transaction đang mở, kết thúc run nếu DB còn hoạt động; crash trước cleanup được startup xử lý. Output đến sau timeout/terminal state không được commit.
- App đóng request không bảo đảm runtime đã dừng inference. Giới hạn một run là giới hạn logic của app; người học cần kiểm runtime trước retry sau timeout, tránh tranh tài nguyên.

## 3. Phụ thuộc ngoài ứng dụng

- **PostgreSQL local:** lưu bền dữ liệu; process hoặc container với volume bền và port chỉ loopback. DB mất kết nối → DATABASE_UNAVAILABLE; không nhận đã lưu khi chưa commit.
- **Runtime local + model:** ứng viên Qwen 4B/7B; LM Studio chỉ là runtime tham chiếu. Model ID, phiên bản, quantization — cách giảm độ chính xác số để giảm tài nguyên — RAM/VRAM/context thật: `TODO(developer)`. Thiếu model chỉ chặn tác vụ AI.
- **Thư viện runtime đề xuất:** Python 3.12; FastAPI/Pydantic, Uvicorn, Jinja2, HTTPX AsyncClient, SQLAlchemy async/psycopg, Alembic. Khóa phiên bản khi tạo pyproject/lock và kiểm tương thích; chưa có manifest chạy được.
- **Fake adapter:** dữ liệu giả định cố định cho tests/offline demo, có nhãn giả lập; không thay bằng kết quả chất lượng model thật.
- **Chuẩn bị môi trường:** cần tải package/model trước, không coi đó là phụ thuộc internet trong mỗi lượt sử dụng. UI assets phục vụ local; ứng dụng có 0 lời gọi cloud trong vận hành MVP.
- **Vận hành:** chủ dự án mở app/DB/runtime và backup DB thủ công. Không thêm autoscaling, Redis, Celery, vector store, MCP hoặc dịch vụ trả phí.

## 4. NFR — Yêu cầu phi chức năng có số đo

**Mọi target mới là đề xuất thiết kế, chưa được người dùng chốt hoặc đo.** Chúng phục vụ kiểm tra kỹ thuật theo yêu cầu này; không khởi động pilot kinh doanh hoặc benchmark chất lượng model đang để sau. p95 là thời gian mà 95% mẫu không vượt quá.

### Quy mô và tài nguyên

- **NFR-S01:** 1 máy, 1 người học, 1 workspace tiếng Anh, 1 Uvicorn worker; tối đa 1 run model running/workspace, 0 hàng đợi model. Kiểm hai yêu cầu model khác ID đồng thời: một chạy, một nhận RUN_BUSY.
- **NFR-S02:** dataset kiểm tra 10.000 history entries; hỗ trợ 5 request đọc/lưu không-model đồng thời trong khi một run đang chờ model. Đây là tải kiểm tra, không giới hạn số hồ sơ lưu cả đời.
- **NFR-S03:** RAM ứng dụng mục tiêu ≤512 MiB, không tính PostgreSQL/runtime/model, trên tải S02. Phần RAM/VRAM model chưa đặt số do chưa biết máy; `TODO(developer)`.
- **NFR-S04:** giữ các giả định SPEC: ≤40.000 UTF-8 bytes context và phải fit context model; ≤3.000 output tokens; ≤500 reports/1.000 events/100 correction notes mỗi kỳ. Vượt nguồn bắt buộc → CONTEXT_LIMIT, không âm thầm cắt nguồn. Giới hạn body HTTP đề xuất 256 KiB, trả 413 PAYLOAD_TOO_LARGE trước receipt claim khi vượt, theo OpenAPI đề xuất ngày 2026-10-08.

### Độ trễ và timeout

- **NFR-L01:** p95 ≤1.000 ms từ nhận request đến response cho lưu hồ sơ/bài và trang lịch sử đầu, trên ít nhất 100 request hợp lệ sau warm-up, dataset S02. Đo cả khi model idle và khi đang inference; máy/DB phải đang hoạt động.
- **NFR-L02:** deadline run 120 giây, tổng tối đa 2 attempts nằm trong cùng deadline. Attempt thứ hai chỉ cho lỗi kết nối/5xx hoặc sửa JSON/quote và còn thời gian; 0 auto retry inference timeout. Chưa cam kết p95 thành công của model.
- **NFR-L03:** mục tiêu response AI ≤125 giây gồm tối đa 5 giây cleanup/DB; timeout browser 130 giây. Database hỏng sau inference phải báo lỗi, không báo đã lưu. Budget CRUD handler 5 giây, browser 10 giây là đề xuất.
- **NFR-L04:** timeout kết nối model 5 giây; app bọc deadline toàn run bằng đồng hồ monotonic. Timeout read của HTTPX là chờ một chunk, không thay deadline tổng; tham chiếu [HTTPX timeouts](https://www.python-httpx.org/advanced/timeouts/).

### Bảo mật và quyền riêng tư

- **NFR-Q01:** 0 endpoint ứng dụng/DB/runtime được publish ra mạng ngoài loopback; 0 CORS wildcard; 0 redirect/cloud fallback từ adapter. Host allowlist, Origin cùng origin và CSRF áp dụng cho mọi POST tool; session signed, HttpOnly, SameSite=Strict.
- **NFR-Q02:** 0 sửa mục tiêu/trạng thái/bài gốc do model; 100% kết quả lưu qua validator. Kiểm ít nhất 6 ca: chỉ dẫn độc trong bài, trong tài liệu, output yêu cầu ghi đè, Origin lạ, workspace reference sai và raw HTML độc. Tất cả phải không tạo effect trái phép.
- **NFR-Q03:** 0 transcript/raw prompt/reply/secrets trong DB/log/history lâu dài. Ghi chú tự khai báo và yêu cầu đính chính chủ động là dữ liệu được phép giữ, không phải bản sao mọi tin nhắn.
- **NFR-Q04:** đề xuất chat buffer tối đa 8 messages/tab, server reply cache TTL ≤10 phút, metadata logs ≤30 ngày. Reload/restart mất reply tạm; cache hết hạn → RESULT_EXPIRED, không gọi lại model cho cùng request.
- Máy local không tạo cách ly với quản trị viên, mã độc hoặc người có quyền đọc file/DB. Chính sách log của runtime phải kiểm tra riêng; app không bảo đảm phần mềm runtime không lưu prompt. Chưa có auth nhiều người dùng hoặc mã hóa DB riêng.

### Khả dụng và toàn vẹn

- **NFR-A01:** mục tiêu ≥99% probe đọc hồ sơ hợp lệ thành công trong phiên 60 phút, 1 probe/5 giây (720 probes), máy/app/DB được bật; model có thể tắt. Không phải SLA 24/7 hoặc uptime tháng.
- **NFR-A02:** RTO — thời gian khôi phục — mục tiêu ≤5 phút sau operator restart app khi DB đã khỏe. 100% run đang chạy trước app crash được chuyển interrupted trước nhận request model mới; không cần tải transcript để phục hồi.
- **NFR-A03:** RPO — lượng dữ liệu có thể mất — 0 bản ghi đã commit khi chỉ app crash và DB/storage còn khỏe; kiểm tại ít nhất 5 điểm trước/sau commit. Không áp dụng cho mất ổ đĩa hoặc hỏng DB.
- **NFR-A04:** trước migration có dữ liệu thật, cần 1 backup thành công và 1 lần restore thử sang DB khác, đối chiếu 100% IDs/counts của dữ liệu kiểm tra. Mất storage chỉ phục hồi đến backup gần nhất; không có backup tự động hoặc cam kết RPO theo giờ.
- **NFR-A05:** 100% ca duplicate request/version conflict trong test giữ một effect hợp lệ, 0 ghi đè journal revision cũ; không giữ DB transaction qua inference.

**Cách kiểm chứng khi có implementation:** unit/contract tests với fake adapter; integration tests với PostgreSQL riêng; E2E cho US-001–US-018; script tải/latency và đo RAM trên fixture S02; smoke local ghi model/máy/latency thực. NFR chưa đạt phải được ghi cùng nguyên nhân và đề nghị điều chỉnh, không tự đổi target. Không thêm dashboard/metrics service.

## 5. Sơ đồ Mermaid

Nguồn sơ đồ: [docs/diagrams/high-level-architecture.mmd](../diagrams/high-level-architecture.mmd). Các khối trong FastAPI là module cùng process; PostgreSQL và runtime là process local riêng. Đường fake chỉ dành cho tests. Sơ đồ không biểu thị cloud hoặc worker queue.

## 6. Quyết định cần ADR

ADR — bản ghi quyết định kiến trúc — ghi lựa chọn, phương án thay thế, mặt bất lợi và điều kiện xem xét lại. Sáu bản ghi được tạo với **Status: Proposed**; yêu cầu nghiệp vụ đã chốt vẫn được ghi như ràng buộc, không coi triển khai là đã được duyệt.

1. [001-modular-monolith.md](adr/001-modular-monolith.md): một backend FastAPI và web cùng origin.
2. [002-postgres-durable-records.md](adr/002-postgres-durable-records.md): PostgreSQL, transaction ngắn, bất biến/phiên bản/idempotency.
3. [003-bounded-model-requests.md](adr/003-bounded-model-requests.md): request-response có giới hạn, async I/O, không task queue.
4. [004-local-model-adapter.md](adr/004-local-model-adapter.md): runtime local qua HTTP, fake adapter và ranh giới quyền model.
5. [005-ephemeral-chat-versioned-journals.md](adr/005-ephemeral-chat-versioned-journals.md): chat RAM, ghi chú ngắn, nhật ký nguồn/phiên bản.
6. [006-localhost-security.md](adr/006-localhost-security.md): loopback, Host/Origin/CSRF/session và kiểm dữ liệu bằng code.

**Cần ADR khi có đủ dữ liệu, chưa quyết định ở đây:** phiên bản Qwen/runtime/quantization trên máy thật; chuyển API hoặc fine-tuning nếu thực sự chọn. Owner: `TODO(project owner)`. Không tạo ADR “Accepted” cho lựa chọn chưa chốt.

**Bàn giao:** triển khai theo I-01–I-07 của SPEC: shell/DB → hồ sơ/tài liệu → bài/lịch sử → sửa bài → chat → nhật ký → kiểm toàn luồng. Dùng các ID US-001–US-018 của tài liệu stories để nghiệm thu; ID US-01… trong SPEC là hệ ID cũ. Không cần mở rộng scope hoặc chạy model trước khi làm phần lưu trữ.

