# Coding standards — Python 3.12 / FastAPI

Áp dụng cho StudyCraft; đây là hướng dẫn review thủ công. Tooling lint/format/hooks/CI đã được bỏ theo yêu cầu chủ dự án; chưa có ứng dụng chạy. Cấu trúc dự kiến theo [SPEC §12](../SPEC.md#12-project-structure); nghiệp vụ theo [PRD](../requirements/prd.md), [thiết kế](../architecture/system-design.md) và [OpenAPI](../api/openapi.json).

## Tên và định dạng

- Module, hàm, biến: `snake_case`; class/schema: `PascalCase`; hằng số: `UPPER_SNAKE_CASE`. Test: `test_<behavior>.py`, hàm `test_<behavior>`. Kiểm khi review diff.
- Dùng type hints (khai báo kiểu) cho tham số và kết quả hàm; có annotation không chứng minh kiểu đúng. Comment/docstring bằng tiếng Anh, giải thích lý do hoặc ràng buộc.
- UTF-8, LF, 4 spaces, double quotes; độ rộng mục tiêu 100 ký tự. Nhóm import: thư viện chuẩn, thư viện ngoài, module dự án; bỏ import không dùng. Ngoại lệ cần lý do trong review.

## Cấu trúc và trách nhiệm

```text
src/studycraft/   main; core/; api/v1/; db/; modules/; execution/;
                 integrations/llm/; contracts/; prompts/; web/
web/templates/, web/static/   Giao diện trong package; không chứa logic nghiệp vụ
migrations/      Alembic, thêm theo increment cần triển khai
tests/           unit/, contract/, integration/, e2e/; docs/   Hợp đồng và quyết định
```

- Route xác thực/validate rồi gọi module service; service thực hiện nghiệp vụ/transaction; model adapter xử lý HTTP. Không thêm generic repository hoặc framework khi các module này đã đủ dùng.
- DB/model I/O dùng async client; không gọi I/O đồng bộ trong `async def`. Không giữ transaction trong lúc đợi model. Reviewer kiểm ranh giới này qua code và test liên quan.
- Thay contract/schema phải cập nhật OpenAPI, migration và test liên quan. Giữ bài gốc, feedback và journal revision bất biến theo SPEC.

## Lỗi và logging

- HTTP trả `application/problem+json`, đúng `code/status/retryable` trong OpenAPI. Bắt lỗi cụ thể tại boundary; lỗi chưa biết trả `INTERNAL_ERROR` với thông báo cố định. Không nuốt lỗi hoặc tự retry inference sau timeout/commit không rõ kết quả.
- Log JSON qua `core/logging.py`, một lần cho mỗi lỗi tại boundary: UTC, correlation/request/run ID, tool, workspace, duration, status/code, entity/version; run thêm model/prompt version, attempts, context counts và token counts nếu có.
- `INFO`: bắt đầu/kết thúc; `WARNING`: lỗi xử lý được; `ERROR`: lỗi nội bộ/DB; `DEBUG`: metadata phát triển. Không `print` trong app; không format message bằng f-string.
- Không log nội dung học/chat/prompt/reply, secrets, `str(exc)` hoặc traceback chưa lọc; retention đề xuất 30 ngày theo SPEC. Privacy test dùng dữ liệu đánh dấu và kiểm DB/log; test thường lệ dùng fake adapter, thử model thật là bước riêng.

## Kiểm chứng thủ công

- Trước commit, đọc diff: đúng phạm vi, tên/kiểu/import rõ, không secrets hoặc dữ liệu học cá nhân; hợp đồng và tài liệu khớp nhau.
- Với tài liệu: kiểm JSON, liên kết và tính nhất quán; không cần tạo test ứng dụng để kiểm một sửa đổi tài liệu.
- Khi triển khai I-01, tạo môi trường Python riêng, dependencies và test đầu tiên; ghi lệnh thực sự chạy được vào hướng dẫn setup. Sau mỗi thay đổi hành vi, chạy test liên quan và ghi kết quả/phần chưa kiểm.
- Chưa có linter, formatter, hooks hoặc CI được cấu hình. Chỉ thêm lại khi chủ dự án yêu cầu; quy chuẩn trong guide hiện được kiểm bằng review và các test ứng dụng khi chúng tồn tại.
