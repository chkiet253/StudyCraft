# ADR 001 — Backend modular monolith và web cùng origin

## Status

Proposed — cập nhật cấu trúc 2026-10-13 theo [SPEC §12](../../SPEC.md#12-project-structure). Backend/UI tách thư mục apps/api và apps/web; yêu cầu một người học local đã có trong [PRD](../../requirements/prd.md). Cấu hình triển khai cùng origin vẫn cần kiểm chứng.

## Context

MVP cần lưu hồ sơ, sửa bài, chat và nhật ký; không có nhu cầu scale nhiều người dùng. Chủ dự án chịu trách nhiệm vận hành. [Thiết kế](../system-design.md) yêu cầu CRUD vẫn hoạt động lúc chờ model.

## Decision

Backend Python 3.12/FastAPI tại `apps/api/`, một Uvicorn worker; các domain module gọi hàm trực tiếp. Web Jinja/HTML/CSS/JS tổ chức tại `apps/web/`, giao tiếp API cùng origin. PostgreSQL và runtime model là process local riêng. Worker/AI service trong cây repo là vị trí mở rộng; chưa tách các domain thành microservice hoặc thêm background queue. Dùng async I/O cho DB/model, không chạy inference CPU trong API.

## Alternatives considered (with trade-offs)

- Microservices: triển khai/scale từng nghiệp vụ riêng; thêm network, cấu hình, tracing và transaction liên dịch vụ không cần cho một người dùng.
- SPA riêng: linh hoạt giao diện; thêm build/dependency và cấu hình origin cho các panel MVP đơn giản.
- Nhúng model trong process app: ít endpoint hơn; model chiếm tài nguyên và lỗi/load model ảnh hưởng backend.

## Consequences (positive/negative)

- **Positive:** backend có một ranh giới nghiệp vụ/transaction; thư mục backend và UI tách rõ; cùng origin giữ quy tắc giao tiếp; PostgreSQL transactions giữ thay đổi nghiệp vụ nhất quán.
- **Negative:** thay đổi domain backend vẫn deploy cùng API; tách thư mục UI/API cần cấu hình assets/origin khi triển khai; một API worker không bảo đảm high availability. Runtime cùng máy vẫn tranh RAM/CPU.

## Revisit trigger

Yêu cầu nhiều người học đồng thời, nhiều worker hoặc deploy ra mạng; hoặc NFR-L01 vẫn không đạt sau tối ưu truy vấn và kiểm soát tài nguyên model. Chỉ tách thành phần khi có nhu cầu đo được.

