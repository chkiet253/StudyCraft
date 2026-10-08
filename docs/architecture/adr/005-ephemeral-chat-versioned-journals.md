# ADR 005 — Lưu lịch sử chat và nhật ký có phiên bản

## Status

Proposed — cập nhật 2026-10-08. Người dùng đã chốt lưu chat trong MVP và nhật ký vĩnh viễn; cơ chế kỹ thuật dưới đây còn là thiết kế, chưa triển khai. Thay thế đề xuất chat chỉ ở RAM ngày 2026-10-07. Giữ tên file cũ để không làm hỏng liên kết.

## Context

Người học cần mở lại hội thoại sau khi đóng ứng dụng. Nhật ký là tóm tắt khai báo và hoạt động, không phải bản sao hội thoại. Máy cá nhân chạy local model có context hữu hạn.

## Decision

PostgreSQL lưu chat_threads/chat_messages; tin người dùng commit trước inference, assistant reply và reports commit cùng receipt sau validation. Replay dựng lại từ IDs trong DB; không có TTL reply. Cùng key không gọi lại model hoặc tạo bản ghi trùng. Lượt lỗi/bị ngắt giữ user message và trạng thái, không tạo assistant giả.

Backend lấy cửa sổ lượt thành công gần nhất theo budget; giảm context không xóa lịch sử. Đề xuất ban đầu tối đa 8 tin cũ, developer điều chỉnh qua thử nghiệm. Logs/receipts/run snapshots không chứa raw chat hoặc prompt.

Nhật ký/revisions lưu vĩnh viễn, không job dọn tự động. Giữ trigger đề xuất mở kỳ có nguồn đổi mới tổng hợp; counts từ events, corrections append phiên bản, source signature chống inference trùng. Nhật ký chỉ dùng reports/events/corrections, không dùng toàn transcript.

## Alternatives considered (with trade-offs)

- Chat chỉ RAM: ít storage nhưng mất hội thoại, không đáp ứng quyết định mới.
- Gửi toàn lịch sử cho model: đơn giản bước chọn context nhưng nhanh vượt tài nguyên máy cá nhân.
- Ghi đè summary: ít bảng nhưng mất lịch sử đính chính.
- Scheduler hoặc vector search: thêm vận hành, chưa cần cho MVP.

## Consequences (positive/negative)

- **Positive:** đọc/replay chat sau restart không cần model; giữ journal revisions và nguồn đính chính.
- **Negative:** thêm bảng, phân trang, migration và backup; model không nhớ mọi tin đã lưu. Phải test transaction/recovery, tránh ghi user message trùng.
- OpenAPI/DDL/ER còn thiết kế cũ: đồng bộ theo [SPEC §6/§9/§13](../../SPEC.md) trước I-05, chưa coi contract cũ là sẵn sàng triển khai.

## Revisit trigger

Cần xóa/export/tìm kiếm hội thoại, nhiều người dùng, chạy nhiều worker, hoặc các lần thử chứng minh cửa sổ context không đủ. Không mở rộng scope chỉ vì dự đoán tải tương lai.

