# 🚀 HƯỚNG DẪN NHANH

## Khởi động ngay (30 giây)

### Bước 1: Chạy ứng dụng
```bash
# Cách 1: Sử dụng script (dễ nhất)
start.bat

# Cách 2: Manual
pip install -r requirements.txt
python app.py
```

### Bước 2: Truy cập
- Mở trình duyệt: **http://127.0.0.1:5000**

### Bước 3: Đăng nhập Admin
- Username: **admin**
- Password: **admin123**

---

## 🎯 Các tính năng chính

### 1. Tạo bài viết với ảnh
1. Đăng nhập
2. Click "✍️ Đăng bài"
3. Nhập tiêu đề, nội dung
4. Click "🖼️ Chọn ảnh" để upload
5. Preview ảnh hiện ngay
6. Click "Đăng bài"

### 2. Quản trị Admin
1. Đăng nhập với admin
2. Click "⚙️ Quản trị" trên menu
3. Quản lý:
   - **Users:** Nâng/hạ quyền, xóa user
   - **Posts:** Xem, sửa, xóa tất cả bài viết
   - **Comments:** Xóa comment không phù hợp

### 3. Comment
1. Mở bất kỳ bài viết nào
2. Click "👁️ Xem chi tiết"
3. Viết comment ở cuối trang
4. Click "Gửi bình luận"

### 4. API
```bash
# Test tất cả API
python test_api.py

# Hoặc manual
curl http://127.0.0.1:5000/api/posts
```

---

## 📁 Files quan trọng

| File | Mô tả |
|------|-------|
| `start.bat` | Khởi động nhanh |
| `reset_database.bat` | Reset database |
| `README.md` | Hướng dẫn đầy đủ |
| `API_DOCUMENTATION.md` | Tài liệu API |
| `SUMMARY.md` | Tổng kết dự án |
| `test_api.py` | Test API script |

---

## 🔧 Troubleshooting

### Lỗi: Port 5000 đã được sử dụng
```python
# Sửa trong app.py dòng cuối:
app.run(debug=True, port=5001)
```

### Reset database (xóa tất cả dữ liệu)
```bash
reset_database.bat
```

### Cài lại dependencies
```bash
pip install -r requirements.txt --force-reinstall
```

---

## 📞 Cần trợ giúp?

Xem các file documentation:
1. **README.md** - Hướng dẫn chi tiết
2. **API_DOCUMENTATION.md** - Chi tiết về API
3. **SUMMARY.md** - Tổng quan dự án

---

## ⚡ Quick Tips

- **Admin badge:** ⭐ Hiển thị bên cạnh tên admin
- **Image formats:** PNG, JPG, JPEG, GIF, WEBP (max 16MB)
- **API session:** Cần đăng nhập qua web trước khi dùng API
- **Delete warning:** Xóa bài viết sẽ xóa luôn ảnh và comments

---

**Chúc bạn sử dụng vui vẻ! 🎉**
