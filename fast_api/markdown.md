# **Báo cáo kết quả task R01**

## Chạy ví dụ GET/POST trên python web framework

### 1. Endpoint POST (Tạo profile)

- **URL:** `POST http://127.0.0.1:8000/profile/`

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
  "user_id": 1,
  "data_received": {
    "username": "phat",
    "age": 22,
    "bio": "string"
  }
}
```
*(Hệ thống tự động cấp phát `user_id` tăng dần và lưu thông tin vào database giả lập trong bộ nhớ `db_profiles`)*

---

### 2. Endpoint GET (Lấy thông tin profile theo ID)

- **URL:** `GET http://127.0.0.1:8000/profile/{user_id}`

#### 2.1. Trường hợp tìm thấy profile (Thành công)
**Input:**
- **URL:** `GET http://127.0.0.1:8000/profile/1`

**Output:**
- **Code:** `200 OK`
- **Body:**
```json
{
  "message": "Lấy thông tin thành công",
  "user_id": 1,
  "data": {
    "username": "phat",
    "age": 22,
    "bio": "string"
  }
}
```

#### 2.2. Trường hợp không tìm thấy profile (Lỗi 404)
**Input:**
- **URL:** `GET http://127.0.0.1:8000/profile/999`

**Output:**
- **Code:** `404 Not Found`
- **Body:**
```json
{
  "detail": "Không tìm thấy profile của người dùng này"
}
```

---

### 3. Endpoint GET (Lấy danh sách tất cả profiles)

- **URL:** `GET http://127.0.0.1:8000/profiles/`

**Input:**
- **URL:** `GET http://127.0.0.1:8000/profiles/`

**Output:**
- **Code:** `200 OK`
- **Body:**
```json
{
  "total": 1,
  "profiles": {
    "1": {
      "username": "phat",
      "age": 22,
      "bio": "string"
    }
  }
}
```

---

### 4. Test trường hợp thiếu field (Validation Error)

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

### 5. Giải thích luồng: Request → Validation → Response

```
Client (HTTP Request)
        │
        ▼
[ 1. Request Layer ] (FastAPI nhận HTTP request, parse body JSON / path param)
        │
        ▼
[ 2. Validation Layer ] (Pydantic Schema: UserProfile / Type Hint: user_id: int)
   ├── Hợp lệ? ────────────┐
   │                       │
   ▼ (Không hợp lệ)        ▼ (Hợp lệ)
Trả ngay lỗi 422       Chuyển vào hàm endpoint tương ứng
Unprocessable Entity   thực thi logic xử lý
        │                       │
        │                       ├─ POST: Lưu vào db_profiles, cấp phát user_id
        │                       ├─ GET /profile/{id}: Tra cứu, nếu thiếu trả lỗi 404
        │                       └─ GET /profiles/: Lấy toàn bộ danh sách
        │                       │
        │                       ▼
        │              [ 3. Response Serialization ]
        │              Chuyển Python Dict sang JSON
        │                       │
        └───────────────┬───────┘
                        ▼
                Client nhận Response
```

### Chi tiết các bước:
1. **Request (Gửi yêu cầu):**
   - Client (trình duyệt, Swagger UI `/docs`, Postman hoặc cURL) gửi HTTP request tới các endpoint (`POST /profile/`, `GET /profile/{user_id}`, `GET /profiles/`).
   - Web server (Uvicorn) nhận request thô và chuyển giao cho FastAPI router xử lý.

2. **Validation (Xác thực dữ liệu qua Pydantic & Type Hints):**
   - **Đối với `POST /profile/`:** FastAPI đọc tham số `profile: UserProfile` và kiểm tra qua Pydantic:
     - **Bắt buộc có:** `username` (kiểu chuỗi) và `age` (kiểu số nguyên).
     - **Tùy chọn:** `bio` (chuỗi hoặc `None`).
     - **Nếu dữ liệu không hợp lệ / thiếu field:** Trả ngay lỗi `422 Unprocessable Entity` và dừng luồng, không gọi hàm xử lý.
     - **Nếu hợp lệ:** Dữ liệu JSON được parse thành instance `UserProfile`.
   - **Đối với `GET /profile/{user_id}`:** FastAPI tự động kiểm tra `user_id` phải là số nguyên (`int`), nếu truyền sai kiểu (ví dụ chuỗi chữ) cũng sẽ trả về lỗi `422`.

3. **Thực thi logic & Response (Xử lý nghiệp vụ và phản hồi):**
   - **`POST /profile/`:** Tự động tăng `next_user_id`, chuyển model sang dict bằng `.model_dump()` và lưu trữ vào dictionary `db_profiles[user_id]`. Trả về `user_id` cùng dữ liệu đã lưu.
   - **`GET /profile/{user_id}`:** Kiểm tra `user_id` trong `db_profiles`. Nếu không tồn tại, kích hoạt `HTTPException(status_code=404)` báo lỗi `404 Not Found`. Nếu tồn tại, trả về data người dùng kèm mã `200 OK`.
   - **`GET /profiles/`:** Trả về tổng số lượng và toàn bộ danh sách profiles trong `db_profiles`.
   - FastAPI tự động tuần tự hóa (serialize) Python dictionary kết quả thành định dạng JSON chuẩn gửi về cho Client.
