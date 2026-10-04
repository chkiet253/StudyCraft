# Định nghĩa sản phẩm StudyCraft

## Ý tưởng đã chốt

**StudyCraft — Personal Learning Workspace** là không gian học tập cá nhân giúp người học quản lý nội dung đang học, thực hành theo phương pháp phù hợp và nhận phản hồi cùng đề xuất tiếp theo từ AI dựa trên tài liệu và lịch sử của mình.

Sản phẩm phục vụ bạn trước, mở đầu bằng **Tiếng Anh**, sau đó mở rộng môn và người dùng. Giao diện là **web có chat**; mỗi môn có không gian riêng trong cùng ứng dụng. Người học chủ động khai báo hoặc nộp bài; agent hỗ trợ và đề xuất, còn người học quyết định thay đổi kế hoạch.

Ba mức hỗ trợ được giữ trong hướng sản phẩm: **bài tập → buổi học → kế hoạch nhiều mục tiêu**. Triển khai theo từng bước, ưu tiên vòng sử dụng có thể dùng ngay và kiểm tra được.

## Nghiệp vụ chung cho mọi môn

Phần dùng chung được xác định theo việc người học cần làm, không theo số agent, model hay công nghệ lưu trữ.

| Nhóm nghiệp vụ | Người học cần làm gì | Hệ thống hỗ trợ gì |
| --- | --- | --- |
| **Quản lý việc đang học** | Chọn môn, đặt mục tiêu, khai báo tài liệu và nội dung đang học. | Giữ ngữ cảnh riêng cho từng môn và cho biết người học đang theo đuổi điều gì. |
| **Tổ chức hoạt động học** | Khai báo hôm nay hoặc trong tuần muốn học gì, chọn phương pháp và cập nhật kết quả. | Lưu kế hoạch đơn giản, nhật ký và việc còn dang dở; đưa ra đề xuất phù hợp với nội dung hiện tại. |
| **Thực hành và nhận phản hồi** | Làm bài trong ứng dụng hoặc gửi bài qua chat, hỏi khi gặp khó khăn. | Đọc bài, phản hồi theo tiêu chí của hoạt động, giải thích lỗi và đề xuất bài hoặc bước tiếp theo. |
| **Duy trì việc học** | Quay lại sau gián đoạn, xử lý phần chưa hoàn thành, chọn cách học bù. | Nhắc nhẹ, gợi ý tiếp tục hoặc kiểm tra ngắn; người học chọn hoãn, học bù hay đổi kế hoạch. |
| **Theo dõi và điều chỉnh** | Xem lịch sử, kết quả và phản hồi theo từng môn. | Tổng hợp thông tin để người học nhận ra điểm cần luyện và quyết định điều chỉnh. |

### Những thông tin chung cần quản lý

- **Môn học:** nơi giữ mục tiêu, tài liệu, cuộc trò chuyện và kết quả liên quan.
- **Mục tiêu:** điều người học muốn đạt được; mốc thời gian có thể khai báo nhưng không bắt buộc.
- **Tài liệu:** tên, thông tin mô tả và nội dung người học hoặc người phát triển cung cấp nếu có.
- **Phương pháp học:** cách thực hành được chọn, chẳng hạn luyện viết, ôn từ hoặc làm bài.
- **Hoạt động học:** việc dự định làm trong ngày hoặc tuần, cùng trạng thái do người học cập nhật.
- **Bài nộp và phản hồi:** nội dung thực hành, nhận xét và kết quả theo tiêu chí của từng phần.
- **Đề xuất:** bước học tiếp, lời nhắc hoặc thay đổi kế hoạch để người học xem và quyết định.

Mỗi môn dùng chung cấu trúc này. Khi chuyển môn, ứng dụng giữ cùng cách điều hướng nhưng đổi nội dung, chat, phương pháp và thông số tương ứng; trang tổng quan có thể tập hợp việc đang học của các môn.

## Vòng hoạt động chính

**Khi người học khai báo nội dung, nộp bài hoặc yêu cầu hỗ trợ, StudyCraft xem mục tiêu, tài liệu và lịch sử của môn đang chọn, quyết định phản hồi hoặc đề xuất phù hợp, rồi lưu kết quả tương tác và chỉ áp dụng thay đổi kế hoạch sau khi người học duyệt.**

Một phiên sử dụng điển hình:

1. Chọn Tiếng Anh, khai báo tài liệu hoặc chủ đề và việc muốn làm hôm nay.
2. Thực hành trong ứng dụng hoặc gửi bài qua chat.
3. Agent phản hồi, giải thích điểm cần sửa và đề xuất việc tiếp theo.
4. Người học tiếp tục, chỉnh hoặc từ chối đề xuất.
5. Lần sau mở lại đúng môn để xem lịch sử và tiếp tục từ nội dung đã lưu.

Nhắc theo lịch và tổng kết tự động là bước mở rộng, không phải điều kiện để vòng này hoạt động.

## Tài liệu và mức tự chủ

**Nguồn học liệu:** người phát triển cập nhật danh mục tài liệu; người học có thể chọn tài liệu có sẵn, nhập tên, dán nội dung hoặc tải tài liệu đang học lên. Tệp, ảnh và bài làm đính kèm là tùy chọn.

Nhập tên tài liệu giúp tìm thông tin và gắn ngữ cảnh. Nếu chỉ có tên, hệ thống không mặc định đã biết nội dung sách hoặc đáp án; phản hồi chi tiết cần dựa trên đề bài, bài nộp hoặc nội dung thực sự được cung cấp. Không cần xây kho ebook hay tìm kiếm web rộng để sử dụng bản đầu.

**Quyền hành động:** người học chịu trách nhiệm quản lý thời gian. Agent đưa ra gợi ý vừa sức, nhắc phần chưa hoàn thành hoặc đề xuất cách học bù; không tự tối ưu toàn bộ lịch cá nhân.

| Hành động | Cách xử lý |
| --- | --- |
| Gửi bài, khai báo đã học gì hoặc sửa thông tin trực tiếp | Lưu theo thao tác của người học. |
| Phản hồi bài, giải thích và đề xuất việc học tiếp | Hiển thị và lưu trong lịch sử; người học không phải duyệt chỉ để xem phản hồi. |
| AI trích xuất nhật ký chưa rõ hoặc đề xuất đổi mục tiêu và kế hoạch | Cho người học sửa hoặc duyệt trước khi cập nhật thành thông tin chính thức. |
| Hoãn, học bù, đổi khung giờ hoặc xác nhận đã hoàn thành | Người học lựa chọn; không suy ra hoàn thành chỉ từ lời nhắc. |

## Các tính năng đã hợp nhất

Giá trị và công sức là đánh giá tương đối cho phiên bản dùng cá nhân. Phương án kỹ thuật nằm ở phần riêng; bảng này mô tả hành vi sản phẩm.

| ID | Tính năng | Nhóm nghiệp vụ | Giá trị | Công sức | Quyền của agent | Phụ thuộc | Giai đoạn |
| --- | --- | --- | --- | --- | --- | --- | --- |
| F01 | Không gian từng môn: mục tiêu, tài liệu, chat, nhật ký ngắn và việc học trong ngày hoặc tuần. | Quản lý việc đang học | Cao | Vừa | Đọc, đề xuất | Người học khai báo | MVP, bắt đầu bằng Tiếng Anh |
| F02 | Nộp bài, nhận phản hồi theo tiêu chí, giải thích lỗi và đề xuất bước luyện tiếp. | Thực hành | Cao | Vừa | Đọc, đề xuất | F01; tiêu chí chấm | MVP, một phương pháp |
| F03 | Hỗ trợ trọn buổi học: chọn hoạt động, xử lý điểm vướng, cập nhật kết quả và chuẩn bị buổi sau. | Tổ chức hoạt động | Cao | Vừa | Đề xuất; thay kế hoạch cần duyệt | F01, F02 | v2 |
| F04 | Nhắc ôn, nhắc phần chưa xác nhận và đề xuất hoãn hoặc học bù. | Duy trì việc học | Vừa | Vừa | Đề xuất | Nhật ký; lựa chọn nhắc của người học | v2 |
| F05 | Lịch sử, thông số theo kỹ năng và tổng kết để điều chỉnh cách học. | Theo dõi và điều chỉnh | Cao | Vừa | Đọc, đề xuất | F01, F02; cách đo riêng | Lịch sử ở MVP; tổng kết ở v2 |
| F06 | Thêm phương pháp Tiếng Anh và môn mới vào cấu trúc chung. | Mở rộng thực hành | Cao | Cao | Theo từng hoạt động | Nội dung và tiêu chí riêng | Sau khi kiểm chứng MVP |
| F07 | Đề xuất kế hoạch giữa các môn và nội dung cần ôn, dựa trên thời gian người học khai báo. | Điều phối việc học | Vừa | Cao | Đề xuất; người học duyệt | F03 đến F06 | Sau khi có nhiều môn |
| F08 | Đọc hoặc xuất tài liệu, nhật ký, lịch học qua Notion và Calendar. | Tích hợp học tập | Chưa chứng minh | Cao | Theo quyền được cấp | Có nhu cầu sử dụng thật | Để sau |

## Phần riêng cho Tiếng Anh và lựa chọn MVP

Các phương pháp từng được nêu gồm ôn từ vựng, luyện nói và luyện viết. Mỗi phương pháp cần hoạt động, tiêu chí phản hồi và thông số riêng; không dùng một điểm chung để đại diện cho mọi kỹ năng.

**Chọn cho MVP:** một phương pháp **luyện viết ngắn qua văn bản**. Người học nhận đề trong ứng dụng hoặc nhập đề của mình, nộp bài và nhận phản hồi về đáp ứng đề, tổ chức ý, ngữ pháp và dùng từ; nhận xét cần chỉ rõ ví dụ trong bài. Đây là quyết định thu hẹp bản đầu, không phải giới hạn lâu dài của Tiếng Anh.

**MVP gồm F01 và F02:** không gian Tiếng Anh theo tài liệu, có chat và nhật ký ngắn; luyện viết ngắn với phản hồi và đề xuất bước tiếp. Hai tính năng nối được vòng khai báo, thực hành, nhận phản hồi và quay lại học, đồng thời tránh phụ thuộc xử lý âm thanh, nhiều môn hoặc tích hợp ngoài.

## Đo thành công

- **Quản lý việc học:** người học biết đang học gì và có thể quay lại đúng nội dung mà không khai báo lại toàn bộ ngữ cảnh.
- **Phản hồi bài viết:** nhận xét cụ thể, phù hợp bài nộp và giúp người học sửa bài; theo dõi nhận xét sai hoặc bị người học bác bỏ.
- **Đề xuất:** đo việc người học chấp nhận, chỉnh hoặc từ chối và lý do; không lấy số đề xuất tạo ra làm thành công.
- **Tiến độ từng phần:** dùng kết quả phù hợp với kỹ năng và lịch sử sửa bài; bỏ yêu cầu gắn nhãn mọi bản ghi theo loại bằng chứng.
- **Vận hành:** theo dõi chi phí cho một phiên và một bài được phản hồi để lựa chọn model và hạn mức sử dụng.

Không mặc định số giờ học hay số bài đã nộp chứng minh người học thành thạo. Điểm số của AI, nếu hiển thị, là nhận xét theo tiêu chí của ứng dụng, không phải điểm thi chính thức.

## Phạm vi không làm trong bản đầu

- Theo dõi chi tiết từng trang hoặc chương đọc, bắt buộc đính kèm bằng chứng và một hệ thống phân loại bằng chứng riêng.
- Tự quản lý thời gian, xác định toàn bộ lịch khả thi hay tự dời lịch của người học.
- Kho ebook, truy vấn nội dung sách chỉ từ tên hoặc tìm tài liệu bên ngoài không giới hạn.
- Luyện nói và chấm phát âm, nhiều phương pháp đồng thời, toán hoặc lập trình.
- Nhiều agent, mobile riêng, tích hợp Notion hoặc Calendar và đồng bộ hai chiều.
- Hệ thống SaaS hoàn chỉnh và kết luận nắm vững kiến thức chỉ từ nhật ký.

## Năm rủi ro và điểm cần kiểm chứng

1. **Chất lượng phản hồi:** agent có thể nhận xét sai hoặc sửa làm đổi ý; cần tiêu chí rõ và kiểm tra các nhận xét trên một bộ bài có người rà soát.
2. **Thiếu nội dung nguồn:** tên tài liệu chưa đủ để biết đề hoặc đáp án; cần cho người học cung cấp phần liên quan khi thiếu thông tin.
3. **Phạm vi phương pháp:** mỗi phương pháp mới kéo theo cách thực hành và đánh giá mới; mở rộng sau khi phương pháp đầu dùng được.
4. **Chi phí và model:** khả năng chi trả khác nhau giữa người dùng; chi phí theo phiên và chất lượng cần được đo trước khi chọn gói sử dụng.
5. **Công sức ghi nhận:** nếu khai báo và duyệt quá nhiều, người học sẽ bỏ dùng; bản đầu cần ít trường bắt buộc và giữ được ngữ cảnh đã biết.

## Định hướng kỹ thuật sau nghiệp vụ

- Bản đầu dùng một agent; nhiều agent là phương án mở rộng cần được chứng minh bằng kết quả.
- Giao diện web có chat; ngữ cảnh và lịch sử được quản lý theo môn trong cùng ứng dụng.
- Model có thể dùng API trả phí, API miễn phí hoặc model local tùy chất lượng và chi phí; không chốt nhà cung cấp ở bản nghiệp vụ và không mặc định miễn phí là đủ chất lượng.
- Python, FastAPI và PostgreSQL là stack đã được đề xuất, chưa phải điều kiện của định nghĩa sản phẩm.
- Cần lưu ngữ cảnh, trạng thái tương tác, quyền duyệt và lịch sử thực thi; MCP, vector search hay framework agent chỉ chọn khi thiết kế kỹ thuật chứng minh cần thiết.

**Trạng thái:** đã chốt định nghĩa sản phẩm và đề xuất MVP cho StudyCraft; bước tiếp theo là đặc tả luồng người dùng và tiêu chí nghiệm thu cho F01, F02.
