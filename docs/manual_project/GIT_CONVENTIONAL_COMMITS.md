# Quy chuẩn commit message (Conventional Commits)

Tài liệu này quy định cách viết commit message trong StudyCraft. Cú pháp và ý nghĩa cốt lõi tuân theo [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/). Các giới hạn độ dài và cách viết subject ở mục 3 là quy ước của project, không phải yêu cầu bắt buộc của đặc tả.

## 1. Cấu trúc

```text
<type>[optional scope][!]: <description>

[optional body]

[optional footer(s)]
```

- `type` bắt buộc và là danh từ, cho biết mục đích chính của commit. StudyCraft thống nhất viết type bằng chữ thường. Đặc tả không phân biệt hoa thường khi đọc các thành phần, ngoại trừ `BREAKING CHANGE` phải viết hoa.
- `scope` tùy chọn, là danh từ đặt trong ngoặc đơn để chỉ module hoặc phần code bị ảnh hưởng, ví dụ `feat(auth):`. Chỉ thêm scope khi nó giúp người đọc hiểu phạm vi thay đổi.
- `!` tùy chọn, đặt ngay trước dấu `:` để đánh dấu thay đổi không tương thích ngược.
- `description` bắt buộc, là tóm tắt ngắn ngay sau `: `.
- `body` tùy chọn, cung cấp bối cảnh, lý do hoặc tác động.
- `footer` tùy chọn, dùng để đánh dấu breaking change hoặc tham chiếu issue/commit.

## 2. Các loại commit dùng trong project

| Type | Khi sử dụng |
|---|---|
| `feat` | Thêm tính năng mới. |
| `fix` | Sửa lỗi. |
| `docs` | Thêm hoặc sửa tài liệu. |
| `style` | Chỉnh định dạng, không thay đổi logic. |
| `refactor` | Tái cấu trúc mà không thêm tính năng hoặc sửa lỗi. |
| `perf` | Cải thiện hiệu năng. |
| `test` | Thêm hoặc sửa kiểm thử. |
| `build` | Thay đổi hệ thống build hoặc dependency. |
| `ci` | Thay đổi cấu hình CI/CD. |
| `chore` | Công việc bảo trì khác. |
| `revert` | Hoàn tác commit trước đó; nên tham chiếu commit bị hoàn tác. |

Đặc tả yêu cầu dùng `feat` cho tính năng mới và `fix` cho sửa lỗi. Các type còn lại là những quy ước phổ biến được StudyCraft chấp nhận; đặc tả cho phép project định nghĩa thêm type. Đặc tả không định nghĩa riêng ngữ nghĩa của `revert`; trong StudyCraft, dùng type này và tham chiếu commit bị hoàn tác. Ngoài breaking change, các type khác không tự mang ý nghĩa phiên bản SemVer.

## 3. Quy ước viết trong StudyCraft

- Mỗi commit tập trung vào một thay đổi logic rõ ràng; nếu có thể, tách các thay đổi độc lập thành commit riêng.
- Viết description theo thể mệnh lệnh, bắt đầu bằng chữ thường và giữ ngắn gọn. Ví dụ: `add`, `fix`, `update`.
- Subject nên dài tối đa 50 ký tự khi có thể và không kết thúc bằng dấu chấm. Đây là mục tiêu về phong cách, không phải giới hạn của đặc tả.
- Nếu có body, ngăn cách body với subject bằng một dòng trống. Body giải thích lý do hoặc tác động thay vì lặp lại diff; nên giới hạn mỗi dòng khoảng 72 ký tự.
- Nếu có footer, đặt footer sau body bằng một dòng trống. Khi không có body, đặt footer sau subject bằng một dòng trống.

## 4. Breaking change và SemVer

Có thể đánh dấu breaking change theo một trong hai cách:

1. Thêm `!` ngay trước dấu `:`. Phần description phải nêu thay đổi không tương thích.
2. Thêm footer `BREAKING CHANGE: <mô tả>`; cụm `BREAKING CHANGE` phải viết hoa.

Breaking change có thể đi cùng bất kỳ type nào. Có thể dùng cả `!` và footer để làm rõ, dù khi đã có `!` thì footer không bắt buộc.

Nếu project phát hành theo Semantic Versioning, quy ước ánh xạ cơ bản là:

- `fix` tương ứng với bản `PATCH`.
- `feat` tương ứng với bản `MINOR`.
- Commit có breaking change tương ứng với bản `MAJOR`, bất kể type.

## 5. Body và footer

Body là phần văn bản tự do, có thể gồm nhiều đoạn. Footer đặt ở cuối commit message; có thể dùng nhiều footer. Mỗi footer gồm token và giá trị, phân cách bằng `: ` hoặc dấu cách trước `#`, ví dụ `Refs: #104`, `Fixes: #104` hoặc `Refs #104`. Theo đặc tả, token nhiều từ phải nối bằng dấu gạch ngang, như `Reviewed-by:`. Ngoại lệ là `BREAKING CHANGE`; `BREAKING-CHANGE` cũng được đặc tả chấp nhận làm token tương đương. Khi viết footer breaking change, dùng đúng dạng viết hoa `BREAKING CHANGE:`.

## 6. Ví dụ

Commit ngắn:

```text
feat(auth): add Google OAuth2 login
fix(api): handle connection timeout
docs(readme): update deployment instructions
```

Commit có body và footer:

```text
feat(cart): add voucher discounts

Validate promo codes during checkout and support percentage-based and
fixed-amount discounts.

Fixes: #104
```

Breaking change:

```text
feat(api)!: change authentication response format

BREAKING CHANGE: clients must read the user object under data.
```

Hoàn tác có tham chiếu commit:

```text
revert: remove voucher discount validation

Refs: abc1234
```

## 7. Tự kiểm tra trước khi commit

- Type mô tả đúng mục đích chính của thay đổi.
- Subject ngắn, bắt đầu bằng chữ thường và dùng thể mệnh lệnh.
- Commit chỉ gom những thay đổi thuộc cùng một mục đích.
- Breaking change đã được đánh dấu bằng `!` hoặc footer `BREAKING CHANGE:`.
- Body và footer chỉ được thêm khi chúng cung cấp bối cảnh hoặc tham chiếu hữu ích.

Tham khảo đặc tả: [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/).


