# StudyCraft — Khái niệm API

> **Contract delta chưa triển khai — 2026-10-08:** [SPEC v3](../SPEC.md) đã chốt lịch sử chat lưu DB, replay sau restart và giới hạn từ theo loại bài. OpenAPI hiện chưa có các thay đổi này; mô tả cache reply RAM/RESULT_EXPIRED cho chat dưới đây đã bị thay thế. Đồng bộ schema, ví dụ và endpoints trong I-03/I-05 trước coding; không dùng contract cũ cho các luồng đó.

**Status: Proposed — 2026-10-08.** Hợp đồng máy đọc: [openapi.json](openapi.json). Nguồn: [user stories](../requirements/user-stories.md), [schema PostgreSQL](../architecture/database-schema.md), [kiến trúc](../architecture/system-design.md), [SPEC](../SPEC.md). Chưa có API chạy; tài liệu này chỉ giải thích khái niệm, không liệt kê lại endpoints.

## Auth — Session local và CSRF

MVP có một người học trên máy cá nhân. Session — ngữ cảnh phiên trình duyệt — không phải tài khoản hay cơ chế xác minh danh tính nhiều người. Cookie `studycraft_session` có chữ ký; ứng dụng kiểm hạn dùng và workspace được phép trước khi đọc/ghi. UUID workspace do client gửi không tự cấp quyền. Các danh mục developer không chứa dữ liệu riêng.

**Lifecycle đề xuất:** trang HTML cùng origin cấp cookie khi chưa có phiên hợp lệ; phiên còn hợp lệ được tái sử dụng để các tab không làm mất token của nhau. Cookie host-only, Path=/, HttpOnly, SameSite=Strict, Max-Age 28.800 giây; nonce phiên ngẫu nhiên 32 bytes, payload gồm nonce/issued_at/expires_at/workspace_id. Signing secret riêng trong môi trường, tối thiểu 32 random bytes, giữ ổn định qua restart. Kiểm chữ ký HMAC — mã kiểm toàn vẹn bằng khóa bí mật — có nhãn miền riêng cho cookie và CSRF. Không đưa secret vào model, git, logs hoặc trình duyệt.

CSRF — chống request giả mạo từ website khác — là token gắn phiên, có trong HTML cùng origin và RAM của tab, gửi bằng `X-CSRF-Token`. POST cần cả cookie, token và `Origin` đúng scheme/host/port; mọi request cần Host nằm trong allowlist. Cookie sai/hết hạn, token sai hoặc Origin thiếu/khác → 403 FORBIDDEN trước khi nhận thao tác ghi. Mở lại trang để lấy phiên/token hiện tại rồi gửi lại **cùng khóa idempotency** nếu thao tác trước có thể đã chạy.

Secret ổn định giúp phiên/token còn hạn dùng sau restart; reply chat trong RAM vẫn mất. Đổi secret làm phiên cũ vô hiệu; không xóa receipts trong DB. HTTP loopback đề xuất chưa đặt Secure cho cookie; nếu đổi HTTPS thì phải đặt Secure. Không CORS wildcard hoặc truy cập LAN/internet. Thiết kế này không cách ly dữ liệu khỏi người/mã độc có quyền trên cùng máy. Auth lifecycle/TTL là đề xuất cần tests, chưa là tính năng đã triển khai.

## Versioning — Phiên bản hợp đồng

API dùng prefix `/api/v1`; health là kiểm tra vận hành độc lập phiên bản nghiệp vụ. `openapi: 3.1.1` là định dạng tài liệu, `info.version: 1.0.0-draft` là phiên bản hợp đồng đề xuất; SPEC v2 là phiên bản tài liệu trước đó. Ba số này không thay thế nhau. [OpenAPI 3.1.1](https://spec.openapis.org/oas/v3.1.1.html).

OpenAPI đề xuất thay transport toàn-POST cũ bằng GET cho đọc, giữ POST cho ghi; `Idempotency-Key` thay `request_id` trong body, Problem thay Error envelope, thêm `planned_period` từ schema. Tool adapter dùng request_id/Error nội bộ. Các thay đổi được ghi tại `x-design-deltas`; không có alias legacy đã chạy. OpenAPI là hợp đồng HTTP đề xuất; SPEC vẫn là nguồn bất biến nghiệp vụ/provider contracts. P01 đã đồng bộ manifest SPEC về planned_period/INTERNAL_ERROR và quy tắc ánh xạ; adapter/tests chưa được triển khai. HTTP input cho phép thiếu planned_period; adapter điền day trước hash/gọi tool, nội bộ/output luôn có trường này.

Request/success objects từ chối trường lạ. Đổi field name/type/meaning, trường bắt buộc, enum response, hoặc thêm field response làm client strict validator thất bại cần major version mới. Tùy chọn input mới có default và không đổi response cũ có thể tăng minor; sửa mô tả/example không đổi hành vi tăng patch. Không thay rubric của phản hồi đã lưu khi đổi version.

## Errors — Problem và gửi lại thao tác

Lỗi dùng `application/problem+json` theo RFC 9457. StudyCraft chọn yêu cầu đủ `type/title/status/detail/instance` cùng `code/retryable/run_id/correlation_id`; RFC không bắt buộc mọi member này. `type` là URI loại lỗi, `instance` là URN opaque cho lần request; `status` phải bằng HTTP status thật. `code` ổn định cho logic client; `title` cố định theo loại. Client bỏ qua extensions chưa biết. [RFC 9457](https://www.rfc-editor.org/rfc/rfc9457.html#section-3).

```json
{
  "type": "urn:studycraft:problem:version-conflict",
  "title": "Version conflict",
  "status": 409,
  "detail": "Phiên bản đã thay đổi. Hãy đọc lại bản hiện tại.",
  "instance": "urn:studycraft:request:00000000-0000-4000-8000-000000000901",
  "code": "VERSION_CONFLICT",
  "retryable": true,
  "run_id": null,
  "correlation_id": "00000000-0000-4000-8000-000000000901"
}
```

`X-Correlation-ID` là ID riêng mỗi HTTP attempt, khác khóa thao tác; body correlation_id và header phải khớp. Không echo input, secret, stack trace, Pydantic input/value hoặc raw provider error. Câu hỏi làm rõ đính chính đã kiểm có thể trả tạm trong detail; không persist/log câu đó. DB chỉ giữ error metadata; replay có thể dựng detail an toàn chung. run_id chỉ có nếu chính request này đã tạo run.

Codes/HTTP mappings và hướng phục hồi nằm ở `x-error-catalog` trong OpenAPI. Lỗi parse/method/body quá lớn/media type được chặn trước receipt. INTERNAL_ERROR sau claim phải kết thúc receipt/run khi DB khỏe; schema đề xuất mở rộng receipt HTTP 500. Nếu success đã commit thì không ghi đè receipt thành lỗi. Nếu kết quả commit/cleanup chưa rõ do DB hỏng, trả DATABASE_UNAVAILABLE và tra/replay cùng khóa sau phục hồi; không tự chạy thêm lượt.

**Idempotency — gửi lại không thêm tác động:** POST nhận `Idempotency-Key` UUID v4, chuẩn hóa lowercase, dùng làm request_id và run.id khi có model. Khóa dùng chung giữa các tool trong cùng workspace. Hash là tool + body nghiệp vụ sau validate/default/chuẩn hóa UUID; không gồm key, cookie, CSRF hoặc correlation ID. Cùng key/hash replay trước kiểm version hiện tại; khác input/tool → IDEMPOTENCY_CONFLICT. Body có request_id bị từ chối.

Đang chạy trả RUN_BUSY. Terminal failed/interrupted không chạy lại cùng key; người học retry chủ động bằng UUID mới sau xử lý nguyên nhân. `retryable=true` không cấp quyền auto retry model. Khi mất response, trước tiên gửi lại **cùng key/body**; có thể đã commit. Receipts giữ lâu dài, không TTL tự động. Non-chat replay giữ response gốc, kể cả journal status lúc đó; đọc artifact bình thường tính lại stale/current.

IDEMPOTENCY_CONFLICT và RESULT_EXPIRED không ghi đè receipt gốc. RUN_BUSY của cùng key đang chạy cũng không đổi receipt; UUID mới bị gate một-run từ chối sau claim có thể có receipt lỗi 409 riêng, không có run cho UUID đó.

Chat success không lưu reply JSON trong DB; RAM cache ≤10 phút hoặc đến restart. Cache hết → RESULT_EXPIRED, không inference hoặc reports trùng; đọc report/artifact đã lưu vẫn được. Không bật HTTP cache: responses dùng `Cache-Control: no-store`.

## Pagination — Đọc lịch sử theo cursor

Cursor — mốc đọc trang tiếp theo — là `before_id` số nguyên dương. Bỏ tham số để lấy trang đầu, không gửi chuỗi `null`. `limit` mặc định 20, từ 1 đến 50. DB lọc `id < before_id`, sắp ID giảm dần, đọc limit+1 để biết còn trang; response có `items` và `next_before_id`.

Nếu còn trang, next_before_id là ID cuối **đã trả**; hết trang là null. Trang rỗng có items=[] và next_before_id=null. ID có thể có gaps; không dùng timestamp/OFFSET hoặc suy ra tổng số mục từ ID. Các danh sách workspace là snapshots có giới hạn, không được hiểu là toàn bộ lịch sử đã phân trang.

Mỗi history item ghép đúng kind/artifact; nhật ký giữ đúng journal_revision của mục lịch sử. Paging qua nhiều HTTP requests không hứa snapshot cố định; mục mới cần refresh trang đầu. Không trả transcript hoặc contents không được phép trong lịch sử.
