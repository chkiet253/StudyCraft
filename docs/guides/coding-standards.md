# Coding standards — Python 3.12 / FastAPI

Áp dụng cho StudyCraft; cấu hình tooling đã có, cấu trúc ứng dụng vẫn theo [SPEC §12](../SPEC.md#12-project-structure). Quy tắc nghiệp vụ lấy từ [PRD](../requirements/prd.md), [thiết kế](../architecture/system-design.md) và [OpenAPI](../api/openapi.json).

## Tên và định dạng

- Module, hàm, biến: `snake_case`; class/schema: `PascalCase`; hằng số: `UPPER_SNAKE_CASE`. Test: `test_<behavior>.py`, hàm `test_<behavior>`. Ruff kiểm tên hàm/class; tên file/hằng số do review.
- Dùng type hints (khai báo kiểu) cho tham số và kết quả hàm; Ruff kiểm annotation, chưa kiểm tính đúng của kiểu. Comment/docstring bằng tiếng Anh, giải thích lý do hoặc ràng buộc.
- UTF-8, LF, 4 spaces, double quotes; độ rộng mục tiêu 100, theo formatter. Import do Ruff sắp xếp. Không dùng `noqa` rộng; ngoại lệ phải ghi mã rule và lý do.

## Cấu trúc và trách nhiệm

```text
app/          main/config/routes/security; tools/runner; db/models;
              contracts/context/corrections/journals/local_model/observability
app/templates/, app/static/   Giao diện; không chứa logic nghiệp vụ
migrations/   Alembic; scripts/   Công cụ developer
tests/        unit/, integration/, e2e/; docs/   Hợp đồng và quyết định
```

- Route xác thực/validate rồi gọi tool; tool điều phối nghiệp vụ; adapter xử lý I/O. Không thêm service/repository/framework khi module hiện có đủ dùng.
- DB/model I/O dùng async client; không gọi I/O đồng bộ trong `async def`. Không giữ transaction trong lúc đợi model. Reviewer kiểm ranh giới này; Ruff chỉ bắt một số mẫu blocking phổ biến.
- Thay contract/schema phải cập nhật OpenAPI, migration và test liên quan. Giữ bài gốc, feedback và journal revision bất biến theo SPEC.

## Lỗi và logging

- HTTP trả `application/problem+json`, đúng `code/status/retryable` trong OpenAPI. Bắt lỗi cụ thể tại boundary; lỗi chưa biết trả `INTERNAL_ERROR` với thông báo cố định. Không nuốt lỗi hoặc tự retry inference sau timeout/commit không rõ kết quả.
- Log JSON qua `observability`, một lần cho mỗi lỗi tại boundary: UTC, correlation/request/run ID, tool, workspace, duration, status/code, entity/version; run thêm model/prompt version, attempts, context counts và token counts nếu có.
- `INFO`: bắt đầu/kết thúc; `WARNING`: lỗi xử lý được; `ERROR`: lỗi nội bộ/DB; `DEBUG`: metadata phát triển. Không `print` trong app; không format message bằng f-string.
- Không log nội dung học/chat/prompt/reply, secrets, `str(exc)` hoặc traceback chưa lọc; retention 30 ngày. Privacy test dùng dữ liệu đánh dấu và kiểm DB/log; không gọi model thật trong CI.

## Tooling và kiểm chứng

[ruff.toml](../../ruff.toml) là nguồn cấu hình; [.editorconfig](../../.editorconfig) đồng bộ editor; [requirements-dev.txt](../../requirements-dev.txt) pin phiên bản. Chọn Ruff thay Black + isort + Flake8 để giảm cấu hình trùng; tham khảo [Ruff](https://docs.astral.sh/ruff/configuration/).

Trong virtual environment (môi trường Python riêng) 3.12 đã kích hoạt, chạy tại repo root:

```powershell
python -m pip install -r requirements-dev.txt
python -m pre_commit install
python -m ruff check --fix .
python -m ruff format .
python -m pre_commit run --all-files
```

[CI](../../.github/workflows/quality.yml) kiểm lint/format, file bị cấm và test tooling. Test ứng dụng chưa tồn tại: I-01 phải thêm dependencies và job chạy test thật; reviewer yêu cầu test hành vi/lỗi liên quan, không coi lint pass là ứng dụng chạy đúng.
