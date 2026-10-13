# **Báo cáo kết quả task R01**

## Chạy ví dụ GET/POST trên python web framework

### 1. Endpoint POST (Tạo profile)

**Input hợp lệ:**
```json
{
  "username": "phat",
  "age": 22,
  "bio": "string"
}
```

**Output:**
- **Code:** `200 OK`
- **Body:**
```json
{
  "message": "Đã lưu profile thành công",
  "data_received": {
    "username": "phat",
    "age": 22,
    "bio": "string"
  }
}
```

---

### 2. Endpoint GET (Lấy thông tin profile)

**Input:**
- **URL:** `GET http://127.0.0.1:8000/profile/1`

**Output:**
- **Code:** `200 OK`
- **Body:**
```json
{
  "message": "Lấy thông tin thành công",
  "user_id": 1
}
```

---

## 3. Test trường hợp thiếu field (Validation Error)

Trong schema `UserProfile`, hai trường `username: str` và `age: int` là bắt buộc, còn `bio: str | None = None` là tùy chọn.

Khi gửi request POST đến `/profile/` nhưng **thiếu trường bắt buộc `age`**:

**Input:**
```json
{
  "username": "phat",
  "bio": "string"
}
```

**Output:**
- **Code:** `422 Unprocessable Entity`
- **Body:**
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": [
        "body",
        "age"
      ],
      "msg": "Field required",
      "input": {
        "username": "phat",
        "bio": "string"
      }
    }
  ]
}
```

---

## 4. Giải thích luồng: Request → Validation → Response

```
Client (HTTP Request)
        │
        ▼
[ 1. Request Layer ] (FastAPI nhận HTTP request, parse body JSON)
        │
        ▼
[ 2. Validation Layer ] (Pydantic Schema: UserProfile)
   ├── Hợp lệ? ────────────┐
   │                       │
   ▼ (Không hợp lệ)        ▼ (Hợp lệ)
Trả ngay lỗi 422       Chuyển vào hàm endpoint `create_profile`
Unprocessable Entity   thực thi logic xử lý
        │                       │
        │                       ▼
        │              [ 3. Response Serialization ]
        │              Chuyển Python Dict/Model sang JSON
        │                       │
        └───────────────┬───────┘
                        ▼
                Client nhận Response
```

### Chi tiết các bước:
1. **Request (Gửi yêu cầu):**
   - Client (trình duyệt, Swagger UI `/docs`, Postman hoặc cURL) gửi HTTP POST request kèm payload JSON tới endpoint `/profile/`.
   - Web server (Uvicorn) nhận request thô và chuyển giao cho FastAPI router xử lý.

2. **Validation (Xác thực dữ liệu qua Pydantic):**
   - FastAPI đọc tham số của hàm `create_profile(profile: UserProfile)` và dùng Pydantic schema `UserProfile` để kiểm tra:
     - **Bắt buộc có:** `username` (kiểu chuỗi) và `age` (kiểu số nguyên).
     - **Không bắt buộc:** `bio` (chuỗi hoặc `None`).
   - **Nếu THIẾU FIELD hoặc SAI KIỂU DỮ LIỆU:**
     - Pydantic phát hiện lỗi và FastAPI lập tức ngắt luồng xử lý.
     - **Hàm `create_profile` hoàn toàn KHÔNG được gọi**.
     - FastAPI tự động đóng gói lỗi thành response chuẩn `422 Unprocessable Entity` chỉ rõ vị trí field bị thiếu (`loc: ["body", "age"]`) và lý do (`msg: "Field required"`).
   - **Nếu DỮ LIỆU HỢP LỆ:**
     - Dữ liệu JSON được chuyển đổi (parse/cast) thành một instance đối tượng Pydantic `UserProfile` và truyền vào hàm `create_profile`.

3. **Response (Phản hồi kết quả):**
   - Hàm `create_profile` thực thi (lưu trữ database, xử lý nghiệp vụ, v.v.) và trả về một Python dictionary.
   - FastAPI tự động tuần tự hóa (serialize) dữ liệu này thành định dạng JSON chuẩn với mã trạng thái `200 OK` gửi về lại cho Client.
