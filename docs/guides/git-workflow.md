# Git workflow — StudyCraft

Team hiện tại **N = 2**, theo [PRD](../requirements/prd.md), cập nhật 2026-10-08. Hai thành viên tự commit; chủ dự án quyết định push/merge và scope, agent chỉ thực hiện Git khi được yêu cầu. Phân công/review theo [lộ trình sprint](../planning/implementation-roadmap.md). Quy trình hiện tại là thủ công, không có hooks, CI hoặc PR template trong repo; guide không xác nhận thiết lập branch protection trên GitHub.

## Branch và commit

- `main` là nhánh tích hợp theo quy ước đề xuất; task mới có thể dùng nhánh ngắn từ `main`. Nhánh mới do agent tạo: `codex/<slug>`; người dùng: `feat/<slug>`, `fix/<slug>` hoặc `docs/<slug>`. Có thể tiếp tục nhánh `docs` hiện có.
- Kiểm working tree trước khi chuyển nhánh; chỉ stage file thuộc task. Không commit/push `.ai/`, `.env` hoặc runtime outputs; `.env.example` chỉ chứa giá trị giả. [.gitignore](../../.gitignore) hiện chỉ bỏ qua `/.ai/`; phải tự kiểm `.env` và outputs trước stage, bổ sung ignore khi tạo các file đó.
- Commit mới và PR title dùng `<type>[scope][!]: <description>`. Type: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`.
- Tự kiểm header: một space sau `:`, description không rỗng, dòng trống trước body. Chia commit theo thay đổi logic; không gom file ngoài task hoặc sửa lịch sử cũ chỉ để đổi style.
- Description nên ở thể mệnh lệnh, bắt đầu chữ thường, không chấm cuối; subject mục tiêu 50 ký tự, body khoảng 72. Đây là hướng dẫn style, không hard limit. Breaking change dùng `!` hoặc `BREAKING CHANGE:`; reviewer kiểm tác động. Chi tiết: [Conventional Commits](../manual_project/GIT_CONVENTIONAL_COMMITS.md).

## PR và review

- Nếu dùng PR, viết trực tiếp: vấn đề/kết quả, US/ADR hoặc lý do bảo trì, lệnh kiểm chứng/kết quả thật, rủi ro và migration nếu có. Không có template bắt buộc; không dùng dữ liệu học cá nhân trong PR.
- Author tự đọc toàn bộ diff, xử lý feedback và chạy check liên quan sau lần sửa cuối. Review logic, contract, permission, privacy và failure paths; tài liệu chỉ cần kiểm nội dung/JSON/liên kết.
- Phân công đề xuất cho nhóm hai người: chủ dự án review contract, DB và model; thành viên thứ hai review luồng sử dụng và chạy lại test. Author tự kiểm diff; thay đổi nhạy cảm cần chủ dự án xem trước tích hợp. Không tạo branch protection hoặc approval tự động trong task tài liệu này.

## Kiểm trước commit, push và merge

```text
git status --short
git diff
git add -- <file-thuoc-task>
git diff --cached
git diff --cached --check
```

- Chỉ commit sau khi staged diff đúng phạm vi; dùng message như `docs(api): align activity contract`. Chạy test liên quan khi có implementation; không ghi đã pass cho check chưa chạy.
- Commit và push là hai thao tác riêng. Trước push, kiểm remote/branch và các commit sẽ gửi; không force-push lịch sử chung.
- Nếu dùng PR, đề xuất squash một task thành một commit dễ theo dõi; đổi lại không giữ từng commit trung gian. Chủ dự án chọn cách merge; kiểm lại diff/message và giải quyết conflict trước merge.
- Hoàn tác thay đổi đã chia sẻ bằng commit `revert:`. CI, required checks và branch protection chỉ thiết lập khi chủ dự án yêu cầu; hiện không có check `quality` để coi là điều kiện merge.
