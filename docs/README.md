# StudyCraft — Cách đọc docs/

**Cập nhật: 2026-10-08.** Điểm bắt đầu cho nhóm hai người. A là chủ dự án/AI Engineer; B là thành viên cùng phát triển. Tài liệu mô tả yêu cầu và thiết kế dự kiến; không phải bằng chứng ứng dụng đã chạy.

## 1. Đọc lần đầu theo thứ tự này

| Thứ tự | Tài liệu | Đọc để trả lời được |
| --- | --- | --- |
| 1 | [Project overview](getting-started/project-overview.md) | StudyCraft phục vụ ai, MVP làm gì, stack và vai trò A/B là gì? |
| 2 | [PRD](requirements/prd.md) | Vấn đề nào cần giải quyết, điều kiện nghiệm thu là gì, phần nào không thuộc MVP? Đọc cả Assumptions và Open questions. |
| 3 | [Định nghĩa sản phẩm](STUDYCRAFT_PRODUCT_DEFINITION.md) | Luồng học và ranh giới giữa tài liệu, bài nộp, kết quả, chat và nhật ký là gì? |
| 4 | [User stories](requirements/user-stories.md) | Người học thực hiện hành động nào? Given/When/Then — đầu vào/hành động/kết quả mong đợi — của story mình làm là gì? Lần đầu lướt các epic, sau đó đọc kỹ story thuộc task. |
| 5 | [Roadmap](planning/implementation-roadmap.md) | Sprint hiện tại cần demo gì, mình nhận task nào, phụ thuộc nào phải xong trước và điều kiện Done là gì? |
| 6 | [SPEC](SPEC.md) §1–4, §12–14 | Quyết định/giả định nào đang áp dụng, cấu trúc code dự kiến ở đâu, và kiểm tra phần mình làm như thế nào? Các mục kỹ thuật còn lại đọc theo task. |

Sau lượt đọc đầu, mỗi người giải thích ngắn một luồng: **chọn đề → nộp/lưu bài → sửa riêng → mở lại**. Cả hai phải phân biệt được: chat không phải nơi nộp bài; lịch sử chat lưu DB nhưng model chỉ đọc một phần; nhật ký là tóm tắt riêng, giữ các phiên bản vĩnh viễn.

Không cần đọc hết OpenAPI JSON hoặc tất cả ADR trước task đầu tiên. ADR — bản ghi quyết định kiến trúc — giải thích lựa chọn, phương án khác, nhược điểm và khi nào cần xem lại.

## 2. Tìm tài liệu theo câu hỏi

| Câu hỏi | Đọc ở đâu |
| --- | --- |
| Vì sao làm tính năng này, có thuộc MVP không? | [PRD](requirements/prd.md), [định nghĩa sản phẩm](STUDYCRAFT_PRODUCT_DEFINITION.md). |
| Người dùng mong đợi gì, khi nào tính năng đạt? | [User stories](requirements/user-stories.md): acceptance criteria của US liên quan. |
| Ai làm, làm khi nào, phải chờ task nào? | [Roadmap](planning/implementation-roadmap.md), [đồ thị task](diagrams/implementation-task-dependencies.mmd). |
| Thành phần giao tiếp và chịu trách nhiệm thế nào? | [System design](architecture/system-design.md), [diagram tổng thể](diagrams/high-level-architecture.mmd), SPEC §5. |
| Vì sao chọn monolith, DB, runner hoặc local model? | ADR [001](architecture/adr/001-modular-monolith.md), [002](architecture/adr/002-postgres-durable-records.md), [003](architecture/adr/003-bounded-model-requests.md), [004](architecture/adr/004-local-model-adapter.md). |
| Chat/nhật ký lưu gì, có giữ bản cũ không? | SPEC §3/6/9, ADR [005](architecture/adr/005-ephemeral-chat-versioned-journals.md). Tên file ADR còn chữ ephemeral do lịch sử; nội dung đã cập nhật quyết định lưu chat. |
| Endpoint nhận/trả gì, lỗi và pagination ra sao? | [API overview](api/overview.md) để hiểu quy ước; [OpenAPI](api/openapi.json) để xem contract HTTP của operation. Pagination là chia kết quả thành các trang bằng cursor. |
| Bảng/cột/constraint/index và quan hệ là gì? | [Database schema](architecture/database-schema.md), [ER diagram](diagrams/database-er.mmd), SPEC §9. ER diagram là sơ đồ quan hệ bảng. |
| Model được phép làm gì, phải dừng khi nào? | SPEC §6–8/10/11/14 và ADR [006](architecture/adr/006-localhost-security.md). |
| Code đặt đâu, viết và review theo quy tắc nào? | SPEC §12, [coding standards](guides/coding-standards.md), [Git workflow](guides/git-workflow.md); [quy ước commit](manual_project/GIT_CONVENTIONAL_COMMITS.md) khi chuẩn bị commit. |
| Coding agent cần tuân theo hướng dẫn nào? | [AGENTS.md](../AGENTS.md) tại root repo; đây là hướng dẫn làm việc, không thay PRD/contract nghiệp vụ. |

## 3. A/B đọc gì trước mỗi sprint?

| Sprint | Cả hai đọc | A đọc sâu | B đọc sâu |
| --- | --- | --- | --- |
| **0 — Khung và contracts** | Overview, PRD, roadmap Sprint 0; SPEC §3/12; coding/Git guides. | SPEC §5/6/8/9; OpenAPI/schema pending; ADR001/002/004/006 cho R02/R03/T000. | Story liên quan các panel, API overview và examples đã chốt cho T005; README root và service mẫu khi có. |
| **1 — Workspace** | US-001–004 và task Sprint 1. | Workspace/version/idempotency/ownership trong SPEC §6/8/9. | Material/activity input/output, schema workspaces/materials/activities và acceptance của module mình nhận. |
| **2 — Nộp bài** | US-005/006/010/011; quy tắc source của US-008. | WritingPolicy/exercise snapshot, submissions/history và immutable data trong SPEC §6/9. | Schema endpoint chọn đề/nộp/rewrite/history; min/max của policy, errors và retry; cấu trúc UI trong SPEC §12. |
| **3 — Sửa bài** | US-007–009/011/018, SPEC §7 và các tình huống §14. | Provider output, exact offsets/edits, runner/context/failure; ADR003/004. | Feedback schema và fixtures; pending/error/retry/empty corrections; phân biệt fake với local evidence. |
| **4 — Chat** | US-012/013/017/018; SPEC §3/9; ADR005. | Chat transactions/replay/recovery, chọn context và trích reports trong SPEC §6–8. | Chat create/list/read/send schemas sau T000, cursor/thứ tự tin, reload và lỗi của thread đang xem. |
| **5 — Nhật ký** | US-014/015 và phần nhật ký offline của US-011. | Source signature/counts, cache/stale/commit recheck trong SPEC §6/9. | Kỳ ngày/tuần, query fixtures, Journal schema, nhãn nguồn và bản đã lưu khi model off. |
| **6 — Đính chính** | US-016/018 và task Sprint 6. | Correction precedence, expected_revision và regeneration trong SPEC §6/9; ADR005. | Journal-linked action, corrected/clarification/conflict, đọc revision cũ; không gọi thêm chat.send để thực hiện journal.correct. |
| **7 — Bàn giao** | Toàn bộ acceptance còn thiếu; SPEC §10/14/15; roadmap gates. | Recovery/local smoke/backup-restore evidence, limits và blockers. | Browser E2E/setup, README đã kiểm chứng, lỗi có bước tái hiện và bằng chứng từng story. |

Đọc đúng phần được task viện dẫn trước khi research tài liệu ngoài. Tài liệu học FastAPI/SQLAlchemy/LM Studio/Playwright và timebox — giới hạn thời gian research — đã nằm ở roadmap §6; đọc để tạo đầu ra cho task, không học hết framework trước khi bắt đầu.

## 4. Khi tài liệu mâu thuẫn hoặc chưa chốt

- Đọc status/date, Assumptions, Open questions và banner pending trước. **Proposed/Draft** là đề xuất/bản nháp; **TODO(owner)** là chưa quyết định; **Accepted** là quyết định được chấp nhận, vẫn chưa chứng minh đã triển khai.
- Quyết định người dùng mới đã ghi nhận ưu tiên. PRD/định nghĩa sản phẩm giải thích phạm vi; SPEC làm rõ quy tắc kỹ thuật; OpenAPI là contract HTTP; schema là thiết kế DB; roadmap điều phối công việc. Roadmap/diagram không tự thêm requirement hoặc thay hợp đồng.
- **Hiện tại:** OpenAPI/DDL/system design còn những phần baseline cũ được đánh dấu pending SPEC v3. A phải đồng bộ trong R02/T000 trước coding consumer; không dùng quy tắc chat chỉ RAM/trần chung 300 từ đã bị thay thế. Không chọn tài liệu chỉ vì nó có ngày mới hơn hoặc sơ đồ dễ đọc hơn.
- Khi phát hiện lệch, ghi đường dẫn/mục, hai phát biểu mâu thuẫn và task bị ảnh hưởng; chuyển A xử lý phần quyết định. Tiếp tục task độc lập, giữ task phụ thuộc ở Blocked. Không tự chọn một phương án rồi để code/contract khác nhau.
- File/code/commands trong cấu trúc dự kiến không có nghĩa chúng tồn tại hoặc đã chạy. Khi implementation có mặt, kiểm tra code/tests/evidence và cập nhật chỗ lệch; không coi code sai là lý do tự đổi yêu cầu đã chốt.
- IDs `US-001–US-018` thuộc user-stories và roadmap; `US-01–US-09` là nhóm rút gọn trong SPEC. Tra theo nội dung/traceability, không tự ghép chỉ bằng số. Txxx là task triển khai; Rxx là research; I-xx là increment — phần ứng dụng tăng dần — trong SPEC.

## 5. Checklist trước khi nhận task

1. Mở hàng task trong roadmap: owner, dependencies, estimate và DoD — điều kiện hoàn thành.
2. Đọc acceptance của US liên quan; ghi một ca thành công và các ca lỗi cần kiểm tra.
3. Đọc schema input/output và quy tắc nghiệp vụ tương ứng trong SPEC; với HTTP đọc OpenAPI, với DB đọc bảng/FK/index liên quan. Với FE, xác nhận mock đúng contract đã chốt.
4. Kiểm tra pending/TODO và prerequisite: contract chưa sync, policy chưa có số thật, model chưa chạy thì không báo task đã sẵn sàng theo giả định riêng.
5. Giải thích được input → service → DB/model → output, dữ liệu nào được lưu/không được đổi và cách chứng minh Done. Chưa giải thích được thì hỏi A hoặc dùng task research tương ứng.

**Ví dụ B nhận T103 — material service:** đọc US-002 → SPEC §6 (`material.save`, version/ownership/catalog rules) → schema catalog_materials/materials → OpenAPI operation material.save và Workspace read → service mẫu T102/coding standards → acceptance T103. Kiểm lưu, reload, title-only, duplicate catalog, version conflict và workspace sai; không cần nghiên cứu prompt/model cho task này.

Khi thay đổi behavior/contract, cập nhật đúng tài liệu và tests bị ảnh hưởng trong cùng task. Không sao chép toàn PRD/SPEC vào report research; report giữ câu hỏi, evidence và quyết định cùng link nguồn.
