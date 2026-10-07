# ADR 003 — Request model có giới hạn, không task queue

## Status

Proposed — 2026-10-07. Giới hạn tham chiếu kế thừa [SPEC v2](../../SPEC.md), chưa đo trên máy thật.

## Context

Một người học chủ động yêu cầu sửa bài, chat hoặc nhật ký. Không có điều phối tự chạy, scheduler hoặc yêu cầu job sống qua restart. Tác vụ model có thể chậm nhưng CRUD không nên bị chặn.

## Decision

Browser chờ response cuối trong cùng request; backend await local HTTP, không giữ transaction trong lúc chờ. Một run running/workspace, không xếp hàng; run khác nhận RUN_BUSY.

Deadline toàn run 120 giây, tối đa 2 attempts trong budget; chỉ retry connect/5xx hoặc JSON/quote sai nếu còn thời gian. Không auto retry inference timeout. Browser chờ tối đa 130 giây; mục tiêu app trả trong 125 giây. Deadline toàn run riêng với timeout từng pha HTTP; [HTTPX read timeout](https://www.python-httpx.org/advanced/timeouts/) chỉ giới hạn chờ chunk.

Request ID/payload hash dùng replay; terminal failed/interrupted cần UUID mới cho retry chủ động. Startup đánh dấu run còn running là interrupted; không tự tiếp tục. Hủy/timeout không nhận output đến muộn; vẫn giữ bài đã commit.

## Alternatives considered (with trade-offs)

- Durable job queue + worker: giữ job qua restart và trả 202 nhanh; thêm process/broker, polling, retry/cancel và bảo mật state.
- BackgroundTasks trong app: trả response sớm; không cung cấp độ bền qua crash, vẫn cần thêm cơ chế trạng thái.
- Route/client đồng bộ qua threadpool: giảm mã async; chiếm thread trong toàn thời gian chờ model, phải quản lý pool khi có nhiều request.
- Streaming: phản hồi sớm; JSON chưa hoàn chỉnh chưa thể nghiệm thu, thêm luồng UI/parser/cancel.

## Consequences (positive/negative)

- **Positive:** ít thành phần; phù hợp một người học; bounds/replay cho hành vi lỗi rõ ràng.
- **Negative:** người học chờ request lâu; app crash không tự hoàn tất job. Run limit là trạng thái app, không bảo đảm runtime dừng inference khi HTTP đóng; retry sau timeout có thể tranh tài nguyên với inference cũ.

## Revisit trigger

Sau khi thử máy thật, tác vụ hợp lệ thường không hoàn tất trong budget, hoặc có yêu cầu job bền/đa người dùng. Trước khi thêm queue, xem lại model, context và deadline cùng chủ dự án.

