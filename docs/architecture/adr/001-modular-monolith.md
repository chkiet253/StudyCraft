# ADR 001 — Monolith với web cùng origin

## Status

Proposed — 2026-10-07. Yêu cầu một người học local đã có trong [PRD](../../requirements/prd.md); bố trí triển khai này là đề xuất.

## Context

MVP cần lưu hồ sơ, sửa bài, chat và nhật ký; không có nhu cầu scale nhiều người dùng. Chủ dự án chịu trách nhiệm vận hành. [Thiết kế](../system-design.md) yêu cầu CRUD vẫn hoạt động lúc chờ model.

## Decision

Một ứng dụng Python 3.12/FastAPI, một Uvicorn worker; các module gọi hàm trực tiếp. Web Jinja/HTML/CSS/JS cùng origin với API. PostgreSQL và runtime model là process local riêng, không phải các microservice nghiệp vụ. Dùng async I/O cho DB/model, không chạy inference CPU trong app.

## Alternatives considered (with trade-offs)

- Microservices: triển khai/scale từng nghiệp vụ riêng; thêm network, cấu hình, tracing và transaction liên dịch vụ không cần cho một người dùng.
- SPA riêng: linh hoạt giao diện; thêm build/dependency và cấu hình origin cho các panel MVP đơn giản.
- Nhúng model trong process app: ít endpoint hơn; model chiếm tài nguyên và lỗi/load model ảnh hưởng backend.

## Consequences (positive/negative)

- **Positive:** một nơi triển khai và kiểm tra; cùng origin giảm cấu hình giao tiếp; PostgreSQL transactions giữ thay đổi nghiệp vụ nhất quán.
- **Negative:** lỗi process app ảnh hưởng toàn bộ UI/API; thay đổi module vẫn deploy cùng app; một worker không bảo đảm high availability. Runtime cùng máy vẫn tranh RAM/CPU.

## Revisit trigger

Yêu cầu nhiều người học đồng thời, nhiều worker hoặc deploy ra mạng; hoặc NFR-L01 vẫn không đạt sau tối ưu truy vấn và kiểm soát tài nguyên model. Chỉ tách thành phần khi có nhu cầu đo được.

