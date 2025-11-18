# 🌟 Blog System - Hệ Thống Blog Nâng Cao

Hệ thống blog đầy đủ tính năng với upload ảnh, phân quyền Admin/User, comment và REST API.

## ✨ Tính Năng

### 🔹 Tính năng cơ bản
- ✅ Đăng ký / Đăng nhập
- ✅ Tạo, sửa, xóa bài viết
- ✅ Giao diện đẹp, responsive

### 🔹 Upload ảnh
- ✅ Upload ảnh cho bài viết
- ✅ Preview ảnh trước khi đăng
- ✅ Hỗ trợ: PNG, JPG, JPEG, GIF, WEBP
- ✅ Giới hạn kích thước: 16MB

### 🔹 Phân quyền Admin/User
- ✅ Vai trò Admin và User
- ✅ Admin có thể:
  - Quản lý tất cả người dùng
  - Nâng/hạ quyền user
  - Xóa user khác
  - Quản lý tất cả bài viết
  - Quản lý tất cả comment
- ✅ User chỉ sửa/xóa bài viết của mình

### 🔹 Comment
- ✅ Bình luận trên bài viết
- ✅ Hiển thị số lượng comment
- ✅ Xóa comment (owner hoặc admin)
- ✅ Hiển thị thời gian comment

### 🔹 REST API
API đầy đủ cho tích hợp bên ngoài:

**Posts API:**
- `GET /api/posts` - Lấy tất cả bài viết
- `GET /api/posts/<id>` - Lấy 1 bài viết
- `POST /api/posts` - Tạo bài viết mới (cần đăng nhập)
- `PUT /api/posts/<id>` - Cập nhật bài viết (cần quyền)
- `DELETE /api/posts/<id>` - Xóa bài viết (cần quyền)

**Comments API:**
- `GET /api/posts/<id>/comments` - Lấy comment của bài viết
- `POST /api/posts/<id>/comments` - Thêm comment (cần đăng nhập)

**Users API:**
- `GET /api/users` - Lấy danh sách user (chỉ admin)

## 🚀 Cài Đặt

### Yêu cầu
- Python 3.7+
- pip

### Các bước cài đặt

1. **Cài đặt dependencies:**
```bash
pip install -r requirements.txt
```

2. **Chạy ứng dụng:**
```bash
python app.py
```

3. **Truy cập:**
- Mở trình duyệt: `http://127.0.0.1:5000`

## 👤 Tài Khoản Mặc Định

**Admin:**
- Username: `admin`
- Password: `admin123`

⚠️ **Quan trọng:** Đổi mật khẩu admin sau khi cài đặt!

## 📖 Hướng Dẫn Sử Dụng

### Người dùng thường (User)
1. Đăng ký tài khoản mới
2. Đăng nhập
3. Tạo bài viết (có thể upload ảnh)
4. Bình luận trên bài viết
5. Sửa/xóa bài viết của mình

### Quản trị viên (Admin)
1. Đăng nhập với tài khoản admin
2. Truy cập "⚙️ Quản trị" trên menu
3. Quản lý:
   - Người dùng (nâng/hạ quyền, xóa)
   - Bài viết (xem, sửa, xóa tất cả)
   - Comment (xóa comment không phù hợp)

## 🔧 API Usage Examples

### Lấy tất cả bài viết
```bash
curl http://127.0.0.1:5000/api/posts
```

### Tạo bài viết mới (cần session)
```bash
curl -X POST http://127.0.0.1:5000/api/posts \
  -H "Content-Type: application/json" \
  -d '{"title":"Test","content":"Hello World"}' \
  --cookie "session=YOUR_SESSION_COOKIE"
```

### Lấy comment của bài viết
```bash
curl http://127.0.0.1:5000/api/posts/1/comments
```

## 📁 Cấu Trúc Dự Án

```
blog_project/
├── app.py                  # Main application
├── database.db            # SQLite database
├── requirements.txt       # Python dependencies
├── static/
│   ├── css/
│   │   └── style.css     # Styles
│   └── uploads/          # Uploaded images
└── templates/
    ├── base.html         # Base template
    ├── index.html        # Home page
    ├── login.html        # Login page
    ├── register.html     # Register page
    ├── create_post.html  # Create post
    ├── edit_post.html    # Edit post
    ├── post_detail.html  # Post detail with comments
    └── admin.html        # Admin panel
```

## 🔒 Bảo Mật

- Mật khẩu được lưu plain text (⚠️ KHÔNG an toàn cho production)
- Để production, nên:
  - Hash mật khẩu (bcrypt, argon2)
  - Sử dụng SECRET_KEY mạnh
  - Enable HTTPS
  - Thêm CSRF protection
  - Rate limiting cho API

## 🐛 Xử Lý Lỗi

- Database tự động được tạo lần đầu chạy
- Thư mục uploads tự động được tạo
- Admin account tự động được tạo nếu chưa tồn tại

## 📝 Database Schema

### Users
- id (INTEGER PRIMARY KEY)
- username (TEXT UNIQUE)
- password (TEXT)
- role (TEXT: 'admin' hoặc 'user')
- created_at (TIMESTAMP)

### Posts
- id (INTEGER PRIMARY KEY)
- title (TEXT)
- content (TEXT)
- author_id (INTEGER)
- image_path (TEXT, nullable)
- created_at (TIMESTAMP)

### Comments
- id (INTEGER PRIMARY KEY)
- post_id (INTEGER)
- user_id (INTEGER)
- content (TEXT)
- created_at (TIMESTAMP)

## 🎨 Customization

### Thay đổi màu sắc
Chỉnh sửa `static/css/style.css`:
- Primary gradient: `#667eea`, `#764ba2`
- Admin color: `#FFD700`, `#FFA500`

### Thay đổi file upload limits
Trong `app.py`:
```python
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
```

## 📞 Support

Nếu gặp vấn đề, kiểm tra:
1. Python version >= 3.7
2. Dependencies đã cài đúng
3. Port 5000 không bị chiếm
4. Quyền ghi file trong thư mục dự án

## 📄 License

MIT License - Free to use and modify

---

**Developed with ❤️ by GitHub Copilot**
