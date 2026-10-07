# ADR 005 — Chat tạm, nhật ký có nguồn và phiên bản

## Status

Proposed — 2026-10-07. Không transcript lâu dài/không form nhật ký là yêu cầu đã chốt trong [PRD](../../requirements/prd.md); các con số và trigger là giả định.

## Context

Người học khai báo việc đã học qua chat; nhật ký tổng hợp lời khai và hoạt động ứng dụng. Summary có thể sai nên cần đính chính, nhưng không được giả tạo events hoặc làm mất bản trước.

## Decision

Raw chat/reply chỉ RAM: tối đa 8 messages/tab, cache server tối đa 10 phút theo giả định SPEC. Database giữ report ngắn đã kiểm, yêu cầu đính chính có chủ đích và metadata; không transcript/source_quote/prompt snapshots. Metadata logs giữ tối đa 30 ngày.

Nhật ký tổng hợp khi xem kỳ có nguồn đổi; không scheduler. Counts tính từ events bằng code. Source signature và IDs xác định nguồn; cùng nguồn trả bản cũ; nguồn trống/chỉ events không inference. Corrections và revision mới lưu cùng transaction, expected_revision kiểm lại lúc commit. Đính chính ngày được đưa vào tuần liên quan; đính chính tuần không bị chia giả cho ngày.

## Alternatives considered (with trade-offs)

- Lưu toàn bộ chat: dễ xem lại câu chữ; trái yêu cầu không transcript và tăng dữ liệu dư.
- Form nhật ký: dữ liệu có cấu trúc rõ; tăng thao tác và trái luồng khai báo chat đã chọn.
- Cron tự tổng hợp: nhật ký sẵn theo lịch; thêm scheduler/background recovery chưa cần.
- Ghi đè một summary: schema nhỏ hơn; mất lịch sử đính chính và khó biết AI đã thay gì.

## Consequences (positive/negative)

- **Positive:** ít dữ liệu hội thoại dư; nhật ký có nguồn/phiên bản, đính chính không thay events; tránh inference trùng.
- **Negative:** không khôi phục được hội thoại đầy đủ, cache hết hạn không replay reply được. Report có thể mất ý; source/revision logic phức tạp hơn một summary đơn. Nguồn lớn có thể vượt context và phải xem theo ngày.

## Revisit trigger

Người dùng thay yêu cầu retention/chat, cần lịch tổng hợp tự động hoặc thường vượt giới hạn nguồn/context. Mọi thay đổi phải xét dữ liệu thật và nguồn đính chính; không bật transcript ngầm.

