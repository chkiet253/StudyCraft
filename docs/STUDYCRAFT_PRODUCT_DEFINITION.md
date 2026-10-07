# Định nghĩa sản phẩm StudyCraft

Cập nhật ngày 2026-10-06 theo quyết định của người dùng: ưu tiên sửa bài đã hoàn thành, chat hỏi đáp riêng, model local và nhật ký tóm tắt.

## Ý tưởng đã chốt

**StudyCraft — Personal Learning Workspace** là không gian học tập cá nhân để giữ thông tin học tập, tài liệu, bài làm và kết quả sửa bài. Bản đầu phục vụ người dùng hiện tại, bắt đầu bằng Tiếng Anh và phương pháp luyện viết ngắn.

Người học hoàn thành bài rồi nộp tại khu vực luyện viết; agent chỉ sửa lỗi, giải thích ngắn và hiển thị kết quả ở khu vực riêng. Agent không mở hội thoại dài hoặc hỏi tiếp sau mỗi lần sửa; gợi ý mở rộng, ý tưởng hay hơn và bài tiếp theo được để sau.

**Chat là khu vực riêng** để người học chủ động hỏi hoặc khai báo việc đã học. Tài liệu được đưa vào khu vực tài liệu riêng, không gửi qua chat. Nhật ký ngày/tuần là bản tóm tắt từ khai báo và hoạt động học được ghi nhận, không phải bản sao toàn bộ hội thoại và không yêu cầu form nhập nhật ký.

Ba mức hỗ trợ bài tập → buổi học → kế hoạch nhiều mục tiêu vẫn là hướng mở rộng; MVP tập trung sửa bài và giữ được ngữ cảnh sử dụng.

## Vấn đề, giá trị và cách kiểm chứng

**Giả thuyết cần kiểm chứng:** tập trung tài liệu, bài làm và kết quả sửa trong một nơi sẽ giúp người học quay lại đúng bài đang học và giảm việc khai báo lại ngữ cảnh. Chưa có số đo về cách làm hiện tại hoặc mức tiết kiệm thời gian; không coi giả thuyết này là kết quả đã chứng minh.

Pilot cá nhân sẽ ghi nhận thủ công: người học có tìm lại đúng bài và kết quả sửa không, còn phải khai báo lại thông tin nào, lỗi sửa nào bị bác bỏ và thao tác nào gây phiền. Baseline và thời gian quan sát được ghi trước pilot; chưa đặt chỉ tiêu cải thiện phần trăm, điểm thành thạo hoặc chi phí sử dụng model.

## Nghiệp vụ chung cho mọi môn

| Nghiệp vụ | Người học thực hiện | Hệ thống hỗ trợ trong MVP |
| --- | --- | --- |
| Quản lý ngữ cảnh | Khai báo mục tiêu, thông tin học tập và chọn tài liệu. | Giữ thông tin trong không gian môn đang học; MVP chỉ có Tiếng Anh. |
| Quản lý tài liệu | Chọn danh mục, nhập tên/mô tả hoặc dán nội dung tại khu vực tài liệu. | Lưu học liệu riêng với chat; tên tài liệu không chứng minh hệ thống biết nội dung. |
| Tổ chức việc học | Khai báo việc dự định làm ngày/tuần, tự cập nhật trạng thái. | Lưu danh sách việc học và trạng thái do người học chọn. |
| Nộp và sửa bài | Hoàn thành rồi nộp bài tại khu vực luyện viết. | Giữ bài gốc, chỉ rõ lỗi, cách sửa và giải thích; cho lưu bản sửa thành bài mới. |
| Hỏi đáp | Chủ động gửi câu hỏi ở chat riêng khi cần. | Trả lời câu hỏi; không tự mở chat từ kết quả sửa bài. |
| Khai báo và xem nhật ký | Kể việc đã học trong chat; xem tóm tắt ngày/tuần. | Tổng hợp khai báo và hoạt động ghi nhận; phân biệt tự khai báo với hành động ứng dụng quan sát được. |
| Đính chính | Yêu cầu sửa nội dung nhật ký qua chat gắn với bản tóm tắt đang xem. | Lưu bản tóm tắt sửa và giữ bản trước; không bắt nhập lại qua form. |

Thông tin cần quản lý: môn học, hồ sơ học tập, mục tiêu, tài liệu, phương pháp, hoạt động, đề, bài nộp, kết quả sửa và các phiên bản nhật ký tóm tắt. Chat phục vụ tương tác tạm thời; không lưu lâu dài nguyên văn toàn bộ hội thoại. Bài nộp, kết quả sửa và tài liệu vẫn được lưu vì là hồ sơ học tập, không phải transcript chat.

## Vòng hoạt động chính

**Chọn tài liệu/đề → làm bài → nộp tại khu vực luyện viết → xem bản sửa riêng → tự sửa hoặc quay lại học sau.**

1. Chọn Tiếng Anh; dùng thông tin học tập đã lưu hoặc cập nhật khi cần.
2. Chọn tài liệu tại khu vực riêng, nhận đề mẫu hoặc nhập đề của mình.
3. Hoàn thành và nộp bài; hệ thống lưu bài trước khi gọi model.
4. Hệ thống hiển thị lỗi, sửa đổi tối thiểu và giải thích trong khu vực kết quả, giữ nguyên bài gốc.
5. Người học tự chọn lưu bản viết lại, hỏi thêm tại chat riêng hoặc kết thúc.
6. Khi xem nhật ký ngày/tuần, hệ thống tổng hợp thông tin liên quan; việc có bài nộp không tự chứng minh đã hoàn thành kế hoạch hoặc thành thạo.

Nếu model không chạy được, bài đã lưu vẫn còn. Kết quả sửa ghi rõ giới hạn nếu thiếu ngữ cảnh; không bắt người học trả lời tiếp để nhận phần sửa có thể thực hiện.

## Tài liệu và quyền quyết định

Khu vực tài liệu là nơi lưu tên, mô tả và nội dung người dùng cung cấp; developer có thể cập nhật danh mục. **MVP chỉ hỗ trợ chọn danh mục, nhập tên và dán văn bản; upload tệp/ảnh thuộc giai đoạn sau.** Đây chưa phải kho lưu trữ file tổng quát.

Tên tài liệu được lưu để nhận diện ngữ cảnh. Hệ thống chỉ sửa theo đề, bài và nội dung thực sự được cung cấp; không suy đoán nội dung sách hay tìm thông tin bên ngoài chỉ từ tên.

| Hành động | Quy tắc |
| --- | --- |
| Người học lưu thông tin, tài liệu, hoạt động hoặc nộp bài | Lưu theo thao tác trực tiếp, không duyệt thêm lần nữa. |
| Agent sửa bài | Hiển thị bản sửa riêng; không thay bài gốc, không tự tạo kế hoạch hay gợi ý mở rộng. |
| Người học khai báo đã học trong chat | Trích ý chính về việc đã học; không ghi toàn bộ cuộc trò chuyện vào nhật ký. |
| Thông tin khai báo thiếu ngày hoặc có mâu thuẫn không giải quyết được | Hỏi ngắn trong chat hoặc ghi rõ chưa xác định; không tự đoán thành sự thật. |
| Hệ thống tạo nhật ký | Tự lưu bản tóm tắt có nhãn do AI tổng hợp; không bắt duyệt từng khai báo. Không vì vậy mà tự đổi mục tiêu/trạng thái hoạt động. |
| Người học đính chính nhật ký | Đính chính qua chat theo bản đang xem; lưu phiên bản mới và giữ lịch sử tóm tắt. |
| Hoàn thành, hoãn hoặc đổi mục tiêu/kế hoạch | Chỉ cập nhật bằng lựa chọn trực tiếp của người học trong MVP; không có AI tự áp dụng. |

Chi tiết về thời điểm tổng hợp và lưu chat tạm là giả định triển khai trong `docs/SPEC.md`, không phải yêu cầu lưu tất cả dữ liệu tương tác.

## Các tính năng đã hợp nhất

Giá trị/công sức chưa được định lượng bằng pilot; không dùng chúng như số liệu ROI hoặc ước tính tiến độ đã kiểm chứng.

| ID | Tính năng | Phạm vi |
| --- | --- | --- |
| F01 | Không gian Tiếng Anh: hồ sơ/mục tiêu, tài liệu riêng, việc học, chat hỏi đáp/khai báo và nhật ký tóm tắt ngày/tuần. | MVP. |
| F02 | Nộp bài viết hoàn thành, sửa lỗi và giải thích ngắn; kết quả riêng với chat. | MVP; gợi ý mở rộng/ý tưởng tốt hơn/bài tiếp theo để sau. |
| F03 | Điều phối trọn buổi học và chuẩn bị buổi tiếp theo. | Sau MVP. |
| F04 | Nhắc ôn, học bù hoặc nhắc theo lịch. | Sau MVP. |
| F05 | Xem lịch sử bài và bản tóm tắt nhật ký; về sau có phân tích kỹ năng. | Lịch sử và tóm tắt nhật ký ở MVP; dashboard/phân tích tiến bộ để sau. |
| F06 | Thêm phương pháp Tiếng Anh hoặc môn học. | Sau khi kiểm chứng MVP. |
| F07 | Đề xuất kế hoạch giữa các môn. | Sau khi có nhiều môn và nhu cầu thật. |
| F08 | Tích hợp Notion/Calendar hoặc dịch vụ ngoài. | Để sau. |

**MVP gồm F01, F02 và phần lịch sử/tóm tắt nhật ký của F05.** Nhật ký tóm tắt mới thuộc MVP theo quyết định ngày 2026-10-06; không đồng nghĩa có scheduler, báo cáo kỹ năng hay điều phối nhiều mục tiêu.

## Phần riêng cho Tiếng Anh

MVP luyện viết ngắn qua văn bản. Agent sửa lỗi thực sự về ngữ pháp, dùng từ, đáp ứng đề và tổ chức ý; không bắt tạo đủ lỗi ở cả bốn nhóm và không viết lại theo sở thích cá nhân.

Hồ sơ sử dụng cần có mục đích luyện viết, loại bài và trình độ tự khai báo nếu có. Người dùng chưa cung cấp trình độ cụ thể; phải cho chọn “chưa xác định”, không tự gán trình độ. Bộ tiêu chí và ví dụ sửa tối thiểu được định nghĩa trong SPEC; không quy đổi ra điểm thi.

Người học xác nhận ý định của bài và ghi nhận sửa đổi bị bác bỏ. Developer chuẩn bị các bài mẫu và kiểm tra đúng luồng; người rà soát có khả năng đánh giá Tiếng Anh kiểm tra nhận xét khi có thể. Chưa chỉ định một người rà soát cụ thể, nên không tuyên bố chất lượng model đã được xác nhận.

## Đo thành công

- Người học nộp bài và đọc bản sửa mà không phải trao đổi nhiều lượt với agent.
- Tìm lại được tài liệu, bài gốc, kết quả sửa và bản tóm tắt nhật ký.
- Sửa đổi chỉ ra đúng đoạn trong bài, không tự thay đổi ý định hoặc bài gốc.
- Chat và kết quả sửa hiển thị riêng; lưu nhật ký không yêu cầu form hoặc giữ nguyên mọi tin nhắn.
- Nhật ký phân biệt điều tự khai báo với việc ứng dụng ghi nhận; người học có thể đính chính.
- Ghi nhận vấn đề sử dụng thực tế trong pilot cá nhân trước khi đặt KPI cải thiện.

Đánh giá định lượng chất lượng model, đo lỗi bị bỏ sót, so sánh model và tính chi phí được để sau. Kiểm tra cơ bản về lưu bài, đúng trích đoạn, quyền cập nhật và lỗi model vẫn phải thực hiện trong MVP. Không suy ra thành thạo từ số bài, số giờ hoặc nhật ký.

## Phạm vi không làm trong bản đầu

- Agent hội thoại dài để hướng dẫn từng bước trong lúc sửa bài.
- Gợi ý ý tưởng hay hơn, bài tiếp theo hoặc mở rộng nội dung sau mỗi lần sửa.
- Upload PDF/ảnh/audio, OCR, kho ebook hay lưu trữ file tổng quát.
- Lưu lâu dài toàn bộ transcript chat hoặc form tạo nhật ký thủ công.
- Nhà cung cấp Claude/cloud, API tính phí, bảng giá và cơ chế budget theo tiền.
- Benchmark chất lượng định lượng, dashboard kỹ năng hoặc kết luận thành thạo.
- Nhắc theo lịch, tự quản lý thời gian, nhiều môn/phương pháp, nhiều agent, SaaS hoặc tích hợp ngoài.

## Rủi ro và điểm cần kiểm chứng

1. Model local có thể sửa sai hoặc đổi ý; cần ví dụ đối chiếu và cách nhận biết sửa đổi bị bác bỏ.
2. Chưa biết cấu hình máy/model phù hợp; phải đo trên máy thực tế, không cam kết tốc độ hoặc chất lượng trước.
3. Tóm tắt có thể bỏ sót hoặc diễn giải quá mức; cần nhãn nguồn, đính chính và giữ phiên bản tóm tắt trước.
4. Không lưu toàn bộ chat đồng nghĩa không khôi phục được hội thoại đầy đủ; UI phải giải thích rõ, còn dữ liệu học cần thiết được lưu riêng.
5. Công sức khai báo phải được quan sát trong pilot; thêm bước duyệt/form không cần thiết có thể cản trở sử dụng.

## Định hướng kỹ thuật sau nghiệp vụ

- Python 3.12, FastAPI và PostgreSQL; web có các khu vực riêng cho tài liệu, luyện viết/kết quả, chat và nhật ký.
- Model local là lựa chọn MVP; Claude chỉ là hướng mở rộng sau này. Tên model, runtime và cấu hình máy chưa được người dùng chốt.
- Cùng một local model có thể xử lý các tác vụ độc lập: sửa bài, trả lời câu hỏi và tóm tắt. Không cần nhiều agent hoặc tác vụ tự tiếp tục.
- Giữ bài/tài liệu/kết quả và các bản tóm tắt; không thiết kế bộ nhớ transcript vĩnh viễn.
- Không cần MCP, vector search, framework agent hoặc tích hợp ngoài cho vòng sử dụng này.

**Trạng thái:** nghiệp vụ được cập nhật theo quyết định ngày 2026-10-06. Đặc tả triển khai tương ứng là `docs/SPEC.md` v2; các giả định về runtime, giới hạn dữ liệu và pilot vẫn cần kiểm chứng khi triển khai.
