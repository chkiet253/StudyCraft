# StudyCraft — Tổng quan dự án

**Cập nhật: 2026-10-08.** Dành cho người mới tham gia; nguồn là PRD và ghi chú stack. Repo hiện ở giai đoạn đặc tả, chưa chứng minh ứng dụng đã chạy.

## Mục tiêu và phạm vi

Giúp người học tổ chức tài liệu, theo dõi việc học và tiếp tục hành trình qua viết, nghe, nói, đọc. Người dùng đầu tiên là chủ dự án; mục tiêu TOEIC/IELTS và trình độ thuộc từng hồ sơ.

**MVP:** workspace tiếng Anh gồm hồ sơ/mục tiêu, tài liệu dạng văn bản, việc học ngày/tuần; nộp bài viết hoàn thành và nhận bản sửa riêng với chat; lịch sử bài/phản hồi; chat chủ động và nhật ký tóm tắt có đính chính, giữ phiên bản trước.

Luồng chính: **chọn đề → làm/nộp bài → lưu bài gốc → xem sửa lỗi → tự sửa hoặc quay lại sau**. Model lỗi không làm mất bài. Người học quyết định thay đổi mục tiêu/trạng thái; lịch sử chat lưu ngay MVP, nhật ký và revisions lưu vĩnh viễn.

Ưu tiên triển khai vòng nộp–sửa–xem lại trước. Nghe/nói/đọc, upload file, nhắc lịch, tích hợp ngoài và chấm điểm thi thuộc giai đoạn sau.

## Stack và lý do lựa chọn

Các lý do là định hướng thiết kế, chưa phải kết quả chạy thử:

- **Python 3.12:** giảm số ngôn ngữ cần duy trì cho nghiệp vụ và tích hợp model.
- **FastAPI:** gom các thao tác web và xử lý yêu cầu model trong một backend.
- **PostgreSQL:** giữ hồ sơ, bài, phản hồi và các phiên bản nhật ký có quan hệ với nhau.
- **Jinja + HTML/CSS/JavaScript — đề xuất:** giao diện đơn giản, hạn chế thêm hệ thống build frontend trong MVP.
- **Qwen khoảng 4B/7B — ứng viên:** phục vụ hướng thử model local trên máy chủ dự án; phiên bản/cấu hình chưa chốt.
- **LM Studio qua HTTP local — đề xuất:** tách phần chạy model khỏi nghiệp vụ để dễ thay lựa chọn sau này.

Fine-tuning (huấn luyện bổ sung), API LLM và Claude được xử lý riêng, chưa tự đưa vào MVP.

## Nhóm và quyền quyết định

- **A — Chủ dự án/AI Engineer:** quyết định phạm vi, kiến trúc, model và bảo toàn dữ liệu; review các thay đổi kỹ thuật quan trọng.
- **B — Thành viên phát triển cùng nền tảng Data & AI:** làm module backend nhỏ, giao diện và tests; tăng độ khó theo kết quả thực hành, không mặc định chỉ làm Data Analyst.
- **Người rà soát tiếng Anh:** `TODO(project owner)`.

**Nhóm hai người đã xác nhận ngày 2026-10-08.** Quỹ giờ và mức thành thạo Python/SQL/web của từng người: `TODO(A/B)`. [Lộ trình sprint](../planning/implementation-roadmap.md) ghi phân công đề xuất và điều kiện hoàn thành.

## Repo và tài liệu cần đọc

Xem [cách đọc docs/](../README.md) để đi theo thứ tự nhập môn, tìm tài liệu theo câu hỏi và biết A/B cần đọc gì trước mỗi sprint.

Root chứa README, AGENTS và hướng dẫn tại `.agents/skills/`. `docs/requirements/` giữ yêu cầu; `docs/manual_project/` giữ quy ước dự án; `docs/getting-started/` giữ tài liệu nhập môn. Cấu trúc mã nguồn dự kiến nằm trong SPEC.

- [README](../../README.md): giới thiệu repo.
- [AGENTS](../../AGENTS.md): hướng dẫn coding agent.
- [PRD](../requirements/prd.md): mục tiêu, phạm vi, tiêu chí nghiệm thu và quyết định mới.
- [User stories](../requirements/user-stories.md): 18 stories, ưu tiên, phụ thuộc và tiêu chí chấp nhận.
- [SPEC](../SPEC.md): kiến trúc, hợp đồng dữ liệu và kế hoạch triển khai.
- [Định nghĩa sản phẩm](../STUDYCRAFT_PRODUCT_DEFINITION.md): bối cảnh nghiệp vụ và hướng mở rộng.
- [Quy ước commit](../manual_project/GIT_CONVENTIONAL_COMMITS.md): cách ghi commit.
