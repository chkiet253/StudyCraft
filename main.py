from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Khởi tạo ứng dụng FastAPI
app = FastAPI()

# Định nghĩa cấu trúc dữ liệu mong đợi từ người dùng (Schema)
class UserProfile(BaseModel):
    username: str
    age: int
    bio: str | None = None  # Trường này không bắt buộc

# Giả lập database bằng dictionary trong bộ nhớ
# key: user_id (int), value: profile (dict)
db_profiles: dict[int, dict] = {}
next_user_id = 1

# 1. Endpoint GET: Lấy thông tin theo user_id
@app.get("/profile/{user_id}")
async def get_profile(user_id: int):
    if user_id not in db_profiles:
        raise HTTPException(status_code=404, detail="Không tìm thấy profile của người dùng này")
    return {
        "message": "Lấy thông tin thành công", 
        "user_id": user_id,
        "data": db_profiles[user_id]
    }

# 2. Endpoint GET: Lấy danh sách tất cả profile đã tạo (tiện cho kiểm tra)
@app.get("/profiles/")
async def get_all_profiles():
    return {
        "total": len(db_profiles),
        "profiles": db_profiles
    }

# 3. Endpoint POST: Tạo mới thông tin
@app.post("/profile/")
async def create_profile(profile: UserProfile):
    global next_user_id
    user_id = next_user_id
    next_user_id += 1

    # Lưu dữ liệu vào db tạm
    profile_data = profile.model_dump()
    db_profiles[user_id] = profile_data

    return {
        "message": "Đã lưu profile thành công",
        "user_id": user_id,
        "data_received": profile_data
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
