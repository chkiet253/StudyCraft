# ADR 004 — Adapter model local và ranh giới quyền

## Status

Proposed — 2026-10-07. Local-first đã chốt; runtime, model cụ thể và cấu hình còn mở.

## Context

[PRD](../../requirements/prd.md) chọn chạy trên máy chủ dự án, ứng viên Qwen 4B/7B. Fine-tuning/API là phần xử lý riêng. Tests cần chạy mà không phải tải model hoặc trả phí.

## Decision

Một LocalModelClient có hai mode fake/local. Local gọi HTTP JSON loopback theo endpoint Chat Completions; LM Studio là runtime tham chiếu theo [tài liệu chính thức](https://lmstudio.ai/docs/developer/openai-compat/chat-completions). Không dùng API cloud fallback, redirect hoặc tải model tự động.

Feedback, chat, summary và correction dùng prompt/context/output schema riêng. App kiểm schema và trích đoạn; model không gọi tool/SQL/HTTP/shell, không sửa goal/activity/submission. Fake adapter trả dữ liệu cố định có nhãn giả lập.

## Alternatives considered (with trade-offs)

- API LLM ngay: giảm việc chạy model trên máy; thêm chi phí, phụ thuộc mạng và dữ liệu gửi ra ngoài, chưa được chọn.
- Nhúng model bằng thư viện Python: kiểm soát inference gần hơn; tăng dependency/resource/coupling với app.
- SDK/framework agent: tiện tool calling và vòng lặp; mở thêm quyền/cơ chế không cần cho tác vụ sửa bài hẹp.
- Fine-tuning trước app: có thể điều chỉnh hành vi; cần dữ liệu, quy trình và tài nguyên chưa chốt, không giải quyết persistence/UI.

## Consequences (positive/negative)

- **Positive:** logic ứng dụng không phụ thuộc tên model; tests không gọi dịch vụ thật; giới hạn quyền kiểm bằng code.
- **Negative:** thêm cấu hình runtime và xử lý lỗi HTTP; model local chưa được bảo đảm chất lượng hoặc tốc độ. Giao thức tương thích không đồng nghĩa model trả JSON đúng; phải kiểm cache/log của runtime riêng.

## Revisit trigger

Runtime không đáp ứng giao thức, hardware/context không đủ cho tác vụ MVP, hoặc chủ dự án quyết định API/fine-tuning sau kiểm chứng. Phiên bản, quantization và máy thật cần ADR riêng khi lựa chọn cụ thể.

