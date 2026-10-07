# ADR 002 — Hồ sơ bền trong PostgreSQL

## Status

Proposed — 2026-10-07. PostgreSQL đã được chọn; chi tiết persistence dưới đây là đề xuất theo [SPEC v2](../../SPEC.md).

## Context

[PRD](../../requirements/prd.md) yêu cầu giữ bài gốc, đọc lại hồ sơ khi model tắt và đính chính nhật ký có lịch sử. Retry/crash không được tạo effect trùng hoặc ghi đè bản cũ.

## Decision

Một PostgreSQL local với storage bền. Dùng các bảng SPEC mục 9; SQLAlchemy async/psycopg và Alembic là thư viện đề xuất. Bài/feedback bất biến; bản viết lại là submission mới, journal revisions append-only.

Chi tiết schema đề xuất, FK scoped, indexes và query patterns: [database-schema.md](../database-schema.md). Các bổ sung hợp đồng còn mở được ghi riêng trong tài liệu đó.

Artifact, event/history và receipt kết quả ghi cùng transaction. Unique(workspace_id, request_id), payload hash và run running/workspace chặn duplicate; kiểm expected_revision trước commit. Tách transaction trước/sau inference, không giữ kết nối DB trong lúc chờ HTTP. Session riêng cho mỗi request/pha transaction; xem [SQLAlchemy async](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html).

## Alternatives considered (with trade-offs)

- SQLite: ít vận hành hơn cho local; thay stack PostgreSQL đã chốt và cần xem lại driver/migration/test.
- JSON files: dễ đọc; phải tự giải quyết ghi đồng thời, liên kết, atomic update và truy vết phiên bản.
- SQL trực tiếp bằng psycopg: ít dependency hơn ORM; tăng mã ánh xạ/kiểm tra lặp ở các bảng liên quan.
- Một transaction kéo dài qua inference: code nhìn liền mạch; giữ kết nối/khóa trong lúc chờ model và khó xử lý timeout.

## Consequences (positive/negative)

- **Positive:** dữ liệu học độc lập với model; liên kết, unique keys và transaction hỗ trợ kiểm soát toàn vẹn. [PostgreSQL constraints](https://www.postgresql.org/docs/current/ddl-constraints.html).
- **Negative:** phải vận hành DB, migration và backup; ORM thêm kiến thức/dependency; hai pha cần kiểm lại trạng thái khi commit. Giữ phiên bản lâu dài tăng dữ liệu; chưa có UI xóa/export trong MVP.

## Revisit trigger

NFR-S02/L01 không đạt sau indexing và paging, nhu cầu retention/xóa/export được chốt, hoặc cần multi-user. Trước mọi migration có dữ liệu thật phải backup/restore thử; không đổi storage hoặc xóa dữ liệu âm thầm.

