# Sprint 0 — Ghi chú chuẩn bị và research

**Cập nhật: 2026-10-13.** Theo quyết định mới của chủ dự án, Sprint 0 chỉ giữ tài liệu, nghiên cứu và các quyết định chuẩn bị. Code T001, script R03, tests và môi trường tạm đã được gỡ; tài liệu này không xác nhận hiện có ứng dụng hoặc test suite chạy được. Phần triển khai T001 được hoãn, chưa hoàn thành theo DoD coding ban đầu.

## T001 — Chuẩn bị package, app factory và cấu hình

**Owner:** A — chủ dự án/AI Engineer. Nguồn: [roadmap](implementation-roadmap.md), [SPEC §12–13](../SPEC.md#12-project-structure), [coding standards](../guides/coding-standards.md). Đây là ghi chú thiết kế để triển khai sau Sprint 0.

### Task này giải quyết việc gì?

T001 tạo nền tảng để ứng dụng được cài, khởi động và kiểm thử nhất quán trên hai máy. Nó chưa triển khai nộp/sửa bài, chat, nhật ký hoặc kết nối model.

| Nội dung chuẩn bị | Ý nghĩa và lựa chọn dự kiến |
| --- | --- |
| Python package | Cấu hình source/import/build cho backend tại `apps/api/src/` với core/modules/shared và main.py; đường dẫn resources được khai báo trong manifest/config thay vì dựa vào working directory. Chốt Python 3.12 theo stack; phiên bản thư viện cụ thể khóa sau khi coding/kiểm tương thích. |
| App factory | Hàm `create_app` tạo một instance FastAPI. Tests có thể tạo instance riêng với cấu hình riêng; không khởi động app hoặc kết nối dịch vụ ngay khi import module. |
| Lifespan | Vòng đời khởi động/dừng app: tạo tài nguyên cần dùng trước nhận request, đóng tài nguyên khi tắt. DB/model client được bổ sung ở task sở hữu chúng. |
| Cấu hình môi trường | Đọc thông số từ environment hoặc `.env` local; thiếu/sai cấu hình phải báo tên biến rõ, không in giá trị secret. |
| Package resources | Contracts/prompts thuộc apps/api/src/shared/ và đi cùng artifact backend; template HTML/static CSS/JS thuộc artifact apps/web/. Khai báo build/config để đọc được sau đóng gói, không phụ thuộc working directory. Nội dung/tính năng thực tế thêm khi task cần. |
| Cấu trúc repo | Dự kiến `apps/api/src/{core,modules,shared}`, `apps/api/migrations/`, `apps/api/tests/`, `apps/web/`, `packages/`, `evals/`, `pipelines/`, `infra/`, `tests/e2e/`, `scripts/` và `.github/` theo SPEC §12; không tạo thư mục/code giữ chỗ trong Sprint 0. |
| Health | Route kiểm tình trạng dịch vụ. DoD T001 chỉ yêu cầu route tối thiểu; kết nối DB và phản hồi readiness đúng thuộc T002. Không báo DB khỏe khi chưa kiểm DB. |

### Các nhóm cấu hình cần chuẩn bị

- Database: `DATABASE_URL`, PostgreSQL local; kết nối/migration thuộc T002.
- Session: `SESSION_SECRET`, secret ổn định, không hard-code; cơ chế session/CSRF thuộc T004.
- Model: `LLM_MODE`, `LOCAL_LLM_BASE_URL`, `LOCAL_MODEL`; `LOCAL_LLM_API_KEY` chỉ nếu runtime bật xác thực. Fake là kết quả giả dùng cho tests/demo; adapter thuộc T301, không chứng minh model thật hoạt động.
- Vận hành: timezone và giới hạn hữu hạn cho timeout, số lần thử, input/output. Giữ các giá trị trong SPEC là đề xuất cần kiểm khi tích hợp; không tự đặt ngưỡng từ nghiệp vụ trong task này.
- Secrets, model weights, dữ liệu runtime và `.ai/` không đưa vào Git.

**Bằng chứng cần có khi triển khai sau:** package cài trên Python 3.12; import/startup chạy; startup/shutdown độc lập giữa các instance; assets đọc được từ package sau cài đặt; cấu hình thiếu/sai bị từ chối mà không lộ secret. Kiểm wheel — bản package có thể cài — từ thư mục ngoài repo để phát hiện asset bị bỏ sót. Hiện chưa có các deliverable coding này trong repo.

**Lựa chọn/trade-off:** giữ `src` layout và app factory theo SPEC, thay vì file app phẳng; thêm cấu hình đóng gói nhưng kiểm được đúng package đã cài. Chưa thêm CI/hooks/framework agent.

**TODO(A/B):** chọn sprint coding để nhận lại T001–T006 và cập nhật lịch. Tác động: các task cần app/DB/security vẫn chờ nền tảng triển khai; hoàn thành ghi chú chuẩn bị không đóng task coding T001.

## R03 — Khả năng chạy model trên máy A

**Câu hỏi / owner:** Máy A có runtime/model local dùng được qua giao thức MVP không? Owner: A — chủ dự án/AI Engineer. Timebox ban đầu: 4h; chưa đo đủ 4h tải liên tục.

### Task này giải quyết việc gì?

R03 kiểm rủi ro phần cứng và môi trường trước tích hợp model. Runtime là chương trình nạp/chạy model, ví dụ LM Studio; model là bộ trọng số thực hiện suy luận. Quantization là cách giảm độ chính xác lưu trọng số để giảm bộ nhớ, có thể ảnh hưởng chất lượng. Chỉ biết máy có GPU hoặc model xuất hiện trong danh sách chưa chứng minh sửa bài được.

### Bằng chứng quan sát ngày 2026-10-13

| Hạng mục | Kết quả đã đọc trực tiếp |
| --- | --- |
| OS | Windows 11 Home, 64-bit, version `10.0.26200`, build `26200`. |
| CPU | AMD Ryzen 5 5600H; 6 cores, 12 logical processors. |
| RAM | `16,539,729,920` bytes, khoảng 15.4 GiB; từ `Win32_ComputerSystem.TotalPhysicalMemory`. |
| GPU/VRAM | NVIDIA GeForce RTX 3050 Ti Laptop GPU; `4096 MiB` VRAM, driver `566.07` theo `nvidia-smi`; có thêm AMD Radeon tích hợp. VRAM là bộ nhớ riêng của GPU. |
| Python | Đã dùng Python `3.12.14` đi kèm Codex cho khảo sát; không chứng minh Python global đã sẵn sàng. Môi trường project tạm đã gỡ theo yêu cầu. |
| LM Studio | Không thấy process hoặc executable ở các vị trí cài đặt tiêu chuẩn đã kiểm tra. Không kết luận chưa cài ở mọi nơi. |
| Model/version/quantization | Chưa lấy được. Qwen 4B/7B vẫn là ứng viên, chưa chọn/tải; chưa có model card cho lựa chọn thực tế. |

**Cách kiểm đã thực hiện:** đọc OS/CPU/RAM/GPU bằng PowerShell `Get-CimInstance`, VRAM bằng `nvidia-smi`; thử GET `http://127.0.0.1:1234/v1/models`. Kết nối bị từ chối cả trong sandbox và sau kiểm tra ngoài sandbox đã được duyệt. Đây là kết quả tại thời điểm khảo sát, cần kiểm lại khi runtime được khởi động. Script/tests thử nghiệm đã gỡ; không giữ lệnh trỏ tới file đã xóa.

**Kết luận:** endpoint mặc định không sẵn sàng. POST `/v1/chat/completions` chưa chạy; khả năng fit máy, context, thời gian suy luận, JSON output và chất lượng sửa bài thật chưa kiểm chứng. 4 GiB VRAM không đủ để tự kết luận Qwen 4B hoặc 7B chạy phù hợp. Không có model weights hoặc dữ liệu học cá nhân được giữ trong repo.

### Việc cần làm khi tiếp tục research

1. `TODO(A)`: xác định vị trí/phiên bản runtime và bật server loopback — chỉ truy cập trên máy. Tác động: đang chặn kiểm tra kết nối và inference.
2. `TODO(A)`: chọn đúng model ID, model card, phiên bản/quantization. Tác động: chưa thể kết luận nhu cầu RAM/VRAM, context hoặc tốc độ; không tự chuyển API/fine-tuning.
3. Sau khi môi trường sẵn, kiểm danh sách model và một request Chat Completions bằng dữ liệu giả; ghi JSON thực nhận, giới hạn context/output và thời gian quan sát. Có thể thực hiện bằng giao diện runtime hoặc công cụ HTTP có sẵn, không cần giữ code research trong repo.
4. Ghi lỗi, cách dừng khi quá thời gian và phần chưa chứng minh. Một request nhỏ thành công chỉ chứng minh kết nối/inference; chất lượng sửa bài cần R07/T308 với các ca đánh giá riêng.

**Tác động dự án:** Sprint 0 vẫn tiếp tục tài liệu/contract khi runtime chưa sẵn. Fake/mock cho triển khai sau giúp kiểm logic ứng dụng nhưng không chứng minh model local hoặc chất lượng tiếng Anh. T302/T308/R07/T703 vẫn cần bằng chứng tương ứng.

**Nguồn giao thức kiểm tra ngày 2026-10-13:** [LM Studio endpoints](https://lmstudio.ai/docs/developer/openai-compat), [List Models](https://lmstudio.ai/docs/developer/openai-compat/models), [Chat Completions](https://lmstudio.ai/docs/developer/openai-compat/chat-completions). `/models` có thể gồm model đã tải nhưng chưa load khi bật JIT; danh sách model không chứng minh inference.
