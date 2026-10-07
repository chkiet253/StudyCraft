# ADR 006 — Ranh giới bảo mật localhost

## Status

Proposed — 2026-10-07. Local một người học là ràng buộc hiện hành; triển khai các lớp bảo vệ cần tests.

## Context

Ứng dụng xử lý nội dung học/model không tin cậy và dữ liệu cá nhân. Chỉ chạy local không đủ để coi mọi POST từ browser hoặc mọi nội dung model là hành động được phép.

## Decision

App/DB/runtime chỉ bind/publish loopback. Web và API cùng origin; Host allowlist gồm địa chỉ local được cấu hình, không wildcard. POST tool cần Origin đúng scheme/host/port và CSRF token gắn signed HttpOnly SameSite=Strict session. Không auth nhiều tài khoản hoặc reverse proxy trong MVP.

Routes có tool allowlist; workspace references, schema/quotes/versions và quyền ghi được kiểm bằng code. Escape text qua Jinja/textContent, không render HTML model. App chỉ kết nối DB/runtime từ cấu hình; không lấy URL từ chat. Secrets ở môi trường, không commit hoặc log. Runtime prompt logging phải kiểm riêng.

## Alternatives considered (with trade-offs)

- Chỉ bind localhost: cấu hình ít hơn; không giải quyết request chéo origin và quyền bị suy từ nội dung.
- OAuth/multi-user/TLS public ngay: phù hợp dịch vụ mạng; thêm auth, certificate và vận hành ngoài MVP.
- Dựa vào system prompt: ít code; không ngăn output trái schema hoặc ghi database trái quyền.
- Mã hóa DB ở tầng app: thêm bảo vệ dữ liệu at rest; thêm quản lý khóa, chưa có yêu cầu/threat model cụ thể.

## Consequences (positive/negative)

- **Positive:** giới hạn exposure; quyền thay đổi dữ liệu do ứng dụng kiểm, không giao cho model; giữ UI flow không thêm duyệt thừa.
- **Negative:** chưa phù hợp truy cập từ thiết bị khác hoặc nhiều người dùng. Không cách ly khỏi admin/mã độc/người có quyền đọc DB trên cùng máy. Cookie/CSRF cần quản lý bootstrap và tests; app không kiểm soát tất cả log của runtime.

## Revisit trigger

Chia sẻ qua LAN/internet, nhiều danh tính người học, thiết bị không đáng tin, hoặc cần bảo vệ dữ liệu khi máy bị truy cập. Khi đó cần xem lại auth, TLS, secrets và quyền DB trước deploy.

