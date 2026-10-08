# Git workflow — StudyCraft

Team hiện tại **N = 1**, theo [PRD](../requirements/prd.md). Chủ dự án chịu trách nhiệm review/merge. Workflow là quy ước mới; cấu hình GitHub dưới đây cần owner bật, chưa được áp dụng bởi việc thêm file.

## Branch và commit

- `main` là nhánh tích hợp; mỗi task dùng nhánh ngắn từ `main`, một mục đích/PR. Nhánh mới do agent tạo: `codex/<slug>`; người dùng: `feat/<slug>`, `fix/<slug>` hoặc `docs/<slug>`. Nhánh `docs` hiện có được giữ.
- Kiểm working tree trước khi chuyển nhánh; chỉ stage file thuộc task. Không commit/push `.ai/`, `.env` hoặc runtime outputs; `.env.example` chỉ chứa giá trị giả. [Hook](../../.pre-commit-config.yaml) chặn tên file `.ai/` và `.env*`, không thay thế review secrets trong nội dung.
- Commit mới và PR title dùng `<type>[scope][!]: <description>`. Type: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`.
- [Validator](../../scripts/check_commit_message.py) kiểm header, một space sau `:`, description không rỗng và dòng trống trước body. Commit file được bỏ comment/whitespace bằng [git stripspace](https://git-scm.com/docs/git-stripspace), không sửa file. Không quét lịch sử cũ hoặc xác minh ngữ nghĩa footer/breaking change.
- Description nên ở thể mệnh lệnh, bắt đầu chữ thường, không chấm cuối; subject mục tiêu 50 ký tự, body khoảng 72. Đây là hướng dẫn style, không hard limit. Breaking change dùng `!` hoặc `BREAKING CHANGE:`; reviewer kiểm tác động. Chi tiết: [Conventional Commits](../manual_project/GIT_CONVENTIONAL_COMMITS.md).

## PR và review

- Dùng [PR template](../../.github/pull_request_template.md): vấn đề/kết quả, US/ADR hoặc lý do bảo trì, lệnh kiểm chứng/kết quả thật, rủi ro và migration nếu có. Không dùng dữ liệu học cá nhân trong PR.
- Author tự đọc toàn bộ diff, xử lý feedback và chạy check sau lần sửa cuối. Review logic, contract, permission, privacy và failure paths; checklist/template được kiểm thủ công.
- Solo: **0 approval bên ngoài bắt buộc**; self-review qua checklist, AI review hỗ trợ. Khi có ≥2 developer, đổi thành 1 approval từ người khác và dismiss approval khi có commit mới; tác giả không thể tự approve PR. [GitHub review](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/approving-a-pull-request-with-required-reviews).

## CI và merge

- [CI](../../.github/workflows/quality.yml) chạy mọi PR vào `main`, kể cả docs, và push vào `main`: lint/format, file bị cấm, test validator; PR title được đọc từ event JSON, không chèn vào shell. Không bỏ qua check lỗi.
- Bật trên GitHub: PR bắt buộc; required check `quality` sau lần chạy đầu; branch phải cập nhật với `main`; resolve conversations; linear history; cấm force-push/xóa `main`, không bypass. Không bật required approval/approval latest push khi solo. [Branch protection](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches).
- Chỉ bật **Squash and merge**: một commit trên `main`/PR, giảm lịch sử vụn; đổi lại không giữ từng commit trung gian. Trước merge, kiểm squash title đúng PR title đã pass. Xóa task branch sau merge; rollback bằng `revert:` qua PR, không rewrite lịch sử chung.
- App test job phải được thêm ở I-01 và trở thành required check trước merge mã ứng dụng; hiện `quality` chỉ chứng minh tooling. Hook local cài bằng `python -m pre_commit install` ([pre-commit](https://pre-commit.com/#installation)); CI vẫn cần thiết khi clone chưa cài hook.
