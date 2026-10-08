# PRD — StudyCraft

**Bản nháp — 2026-10-08.** Nguồn: [định nghĩa sản phẩm](../STUDYCRAFT_PRODUCT_DEFINITION.md), [SPEC v3](../SPEC.md); quyết định mới trong cuộc trao đổi này được ưu tiên. Chưa phải sản phẩm đã triển khai.

## Problem — Vấn đề

Giả thuyết: tài liệu, bài và phản hồi rời rạc khiến người học khó tiếp tục việc đang học, phải khai báo lại ngữ cảnh. Chưa có số đo xác nhận.

“Cải thiện hành trình học” quá rộng: MVP kiểm chứng khả năng tìm lại ngữ cảnh và hoàn tất vòng sửa bài. Số bài/giờ không chứng minh tăng năng lực.

## Target users/personas — Người dùng mục tiêu

- **Đối tượng dài hạn:** người học muốn theo dõi hành trình qua viết, nghe, nói, đọc.
- **Người dùng đầu tiên — đã chốt:** chính chủ dự án, dùng trên máy cá nhân để theo dõi việc học và sửa bài viết hoàn thành.
- **Định hướng:** TOEIC hoặc IELTS tùy người học. Mục tiêu/trình độ theo từng hồ sơ, cho phép chưa xác định; MVP chưa chấm điểm chuẩn thi.

## Goals + success metrics — Mục tiêu và cách đo

**Điều kiện nghiệm thu từ SPEC; chưa có kết quả kiểm tra:**

- **Sửa bài độc lập:** 0 lượt chat bắt buộc từ nộp bài đến xem kết quả; kiểm tra toàn luồng.
- **Giữ hồ sơ:** 100% ca kiểm tra bài đã lưu giữ nguyên văn sau sửa/retry/restart; tài liệu, phản hồi, nhật ký đọc lại được khi model tắt.
- **Kiểm soát thay đổi:** 0 lần model tự đổi mục tiêu, trạng thái việc học hoặc bài gốc. 100% sửa đổi văn bản được lưu có trích đoạn hợp lệ; chưa chứng minh đúng ngữ nghĩa.
- **Nhật ký ít thao tác:** 0 form nhật ký bắt buộc; 100% ca đính chính/tổng hợp lại giữ bản trước và nội dung đính chính. Chat đã lưu mở lại được sau restart; 0 bản sao raw chat trong log/receipt; nhật ký và revisions không tự hết hạn.

**Đánh giá giá trị:** theo người dùng, để sau khi sản phẩm dùng được. Số đo ban đầu, thời lượng thử, ngưỡng cải thiện chưa chốt; không chặn triển khai ứng dụng. Chưa đặt chỉ tiêu thành thạo, chất lượng model hoặc chi phí.

## MVP scope — Phạm vi MVP

MVP gồm F01, F02 và phần lịch sử/nhật ký của F05:

1. **Workspace tiếng Anh:** hồ sơ/mục tiêu, tài liệu riêng dạng tên/mô tả/văn bản hoặc danh mục; việc học ngày/tuần do người học cập nhật.
2. **Sửa bài hoàn thành:** chọn đề mẫu/đề riêng; lưu bài trước khi gọi model local; hiển thị lỗi, sửa tối thiểu và giải thích riêng. Giữ bài gốc; bản viết lại là bài mới. Giới hạn từ theo loại bài; ngưỡng cụ thể TODO(project owner).
3. **Chat chủ động:** hỏi đáp riêng, có thể chọn bài/phản hồi làm ngữ cảnh; khai báo việc đã học. Không tự mở chat sau sửa bài. Lưu lịch sử trong MVP, mở lại sau reload/restart; xem lịch sử không cần model.
4. **Lịch sử/nhật ký:** xem lại bài/phản hồi; tóm tắt ngày/tuần từ khai báo ngắn và hoạt động ứng dụng, phân biệt hai nguồn. Đính chính qua chat, giữ phiên bản trước; không form nhật ký.

Luồng: chọn đề/tài liệu → làm/nộp bài → xem kết quả → tự sửa hoặc quay lại. Model lỗi: giữ bài đã lưu, báo lỗi, cho thử lại. Không suy đoán nội dung tài liệu từ tên.

**Phạm vi quá lớn:** cả bốn kỹ năng vượt MVP; chat và nhật ký đính chính cũng tăng công sức. Đề xuất làm nộp–sửa–lịch sử trước, rồi chat/nhật ký; không thêm điều phối buổi học.

## Non-goals — Không làm trong MVP

- Nghe/nói/đọc, audio, nhiều môn, nhiều người dùng hoặc SaaS.
- Coaching nhiều lượt, ý tưởng mở rộng, tự sinh bài tiếp theo, tự đổi kế hoạch.
- Upload file/ảnh/PDF, OCR, kho file tổng quát, tìm nội dung sách từ tên.
- Nhắc lịch, tích hợp ngoài, dashboard kỹ năng, điểm thành thạo hoặc điểm thi TOEIC/IELTS.
- Form nhật ký, tìm kiếm/đổi tên/xóa/phân nhánh hội thoại; Claude/cloud, tính chi phí và benchmark chất lượng định lượng.

## Assumptions — Giả định

- **Đã chốt — cập nhật 2026-10-08:** nhóm có hai người xuất phát từ Data & AI/Khoa học Dữ liệu: chủ dự án là AI Engineer, thành viên thứ hai cùng phát triển MVP. Chủ dự án quyết định phạm vi/ưu tiên; năng lực web/backend và quỹ giờ từng người chưa xác nhận. Người rà soát tiếng Anh chưa chỉ định.
- **Đã chốt:** ưu tiên model local trên máy chủ dự án; ứng viên Qwen khoảng 4B hoặc 7B (quy mô tham số), chưa chọn phiên bản hoặc cấu hình cụ thể.
- **Phần model riêng:** fine-tuning (huấn luyện bổ sung) hoặc API LLM là phương án chưa chốt, không chặn xây ứng dụng. Không tự chuyển sang API.
- **Thiết kế dự kiến:** web local, Python 3.12/FastAPI/PostgreSQL. PostgreSQL là hệ quản trị cơ sở dữ liệu; psql là công cụ dòng lệnh làm việc với PostgreSQL.
- **Giả định để chốt sau:** Jinja/HTML/CSS/JS, runtime LM Studio, nhật ký tổng hợp khi xem kỳ có nguồn thay đổi; developer chọn context nhỏ và timeout hữu hạn để thử model. Chưa xác nhận.

## Risks — Rủi ro

- Sửa sai/đổi ý: sửa tối thiểu, giữ bài gốc; cần người rà soát. Kiểm tra phần mềm không xác nhận chất lượng tiếng Anh.
- Model/máy yếu: chưa có cấu hình hoặc kết quả chạy thử; thử máy thật trước cam kết tốc độ, giữ khả năng lưu/xem hồ sơ.
- Nhật ký hiểu sai/bỏ sót: phân biệt nguồn, nhãn AI tổng hợp, hỗ trợ đính chính có lịch sử.
- Lịch sử chat tăng dữ liệu cần backup; model có thể thiếu tin cũ do context hữu hạn. Tách lưu lịch sử khỏi lượng tin gửi model.
- Tài liệu/bài chứa chỉ dẫn độc hại: coi là dữ liệu; không cho đổi quyền hoặc tự cập nhật kế hoạch.

## Open questions — Thông tin để chốt theo giai đoạn

- **Khi xử lý model:** phiên bản Qwen 4B/7B, runtime và cấu hình máy; có cần fine-tuning hay chuyển API không? `TODO(project owner)`.
- **Khi chuẩn bị kiểm chứng chất lượng:** người rà soát tiếng Anh chưa chỉ định. `TODO(project owner)`.
- **Sau khi sản phẩm dùng được:** cách đo giá trị, thời lượng thử, ngưỡng thành công. `TODO(project owner)`.
- **Để sau theo người dùng:** thời hạn giao bản đầu và các giả định triển khai còn tạm thời. `TODO(project owner)`.

Đủ thông tin để triển khai ứng dụng. Model cần chốt trước thử tích hợp; giá trị và chất lượng ngôn ngữ chưa được kiểm chứng.

