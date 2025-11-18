# 📡 API Documentation

REST API đầy đủ cho Blog System

## Base URL
```
http://127.0.0.1:5000/api
```

## Authentication
API sử dụng session-based authentication. Bạn cần đăng nhập qua web interface trước, sau đó sử dụng session cookie.

---

## 📝 Posts Endpoints

### 1. Get All Posts
Lấy danh sách tất cả bài viết.

**Endpoint:** `GET /api/posts`

**Response:**
```json
[
  {
    "id": 1,
    "title": "Bài viết đầu tiên",
    "content": "Nội dung bài viết...",
    "author_id": 1,
    "username": "admin",
    "image_path": "uploads/20251118120000_image.jpg",
    "created_at": "2025-11-18 12:00:00"
  }
]
```

**Example:**
```bash
curl http://127.0.0.1:5000/api/posts
```

---

### 2. Get Single Post
Lấy thông tin 1 bài viết cụ thể.

**Endpoint:** `GET /api/posts/<id>`

**Parameters:**
- `id` (integer) - ID của bài viết

**Response:**
```json
{
  "id": 1,
  "title": "Bài viết đầu tiên",
  "content": "Nội dung bài viết...",
  "author_id": 1,
  "username": "admin",
  "image_path": "uploads/20251118120000_image.jpg",
  "created_at": "2025-11-18 12:00:00"
}
```

**Error Response (404):**
```json
{
  "error": "Post not found"
}
```

**Example:**
```bash
curl http://127.0.0.1:5000/api/posts/1
```

---

### 3. Create Post
Tạo bài viết mới. **Yêu cầu đăng nhập.**

**Endpoint:** `POST /api/posts`

**Headers:**
- `Content-Type: application/json`
- Cookie với session hợp lệ

**Request Body:**
```json
{
  "title": "Tiêu đề bài viết",
  "content": "Nội dung bài viết..."
}
```

**Response (201):**
```json
{
  "id": 5,
  "message": "Post created"
}
```

**Error Response (401):**
```json
{
  "error": "Unauthorized"
}
```

**Error Response (400):**
```json
{
  "error": "Title and content required"
}
```

**Example:**
```bash
curl -X POST http://127.0.0.1:5000/api/posts \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Post","content":"This is a test"}' \
  --cookie "session=YOUR_SESSION_COOKIE"
```

---

### 4. Update Post
Cập nhật bài viết. **Yêu cầu quyền (author hoặc admin).**

**Endpoint:** `PUT /api/posts/<id>`

**Parameters:**
- `id` (integer) - ID của bài viết

**Headers:**
- `Content-Type: application/json`
- Cookie với session hợp lệ

**Request Body:**
```json
{
  "title": "Tiêu đề mới",
  "content": "Nội dung mới..."
}
```

**Response (200):**
```json
{
  "message": "Post updated"
}
```

**Error Responses:**
- `401`: Unauthorized - Chưa đăng nhập
- `403`: Forbidden - Không có quyền
- `404`: Post not found

**Example:**
```bash
curl -X PUT http://127.0.0.1:5000/api/posts/1 \
  -H "Content-Type: application/json" \
  -d '{"title":"Updated Title","content":"Updated content"}' \
  --cookie "session=YOUR_SESSION_COOKIE"
```

---

### 5. Delete Post
Xóa bài viết. **Yêu cầu quyền (author hoặc admin).**

**Endpoint:** `DELETE /api/posts/<id>`

**Parameters:**
- `id` (integer) - ID của bài viết

**Headers:**
- Cookie với session hợp lệ

**Response (200):**
```json
{
  "message": "Post deleted"
}
```

**Error Responses:**
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Post not found

**Example:**
```bash
curl -X DELETE http://127.0.0.1:5000/api/posts/1 \
  --cookie "session=YOUR_SESSION_COOKIE"
```

---

## 💬 Comments Endpoints

### 6. Get Comments for Post
Lấy tất cả comment của 1 bài viết.

**Endpoint:** `GET /api/posts/<id>/comments`

**Parameters:**
- `id` (integer) - ID của bài viết

**Response:**
```json
[
  {
    "id": 1,
    "post_id": 1,
    "user_id": 2,
    "username": "user123",
    "content": "Comment hay quá!",
    "created_at": "2025-11-18 13:00:00"
  }
]
```

**Example:**
```bash
curl http://127.0.0.1:5000/api/posts/1/comments
```

---

### 7. Add Comment
Thêm comment vào bài viết. **Yêu cầu đăng nhập.**

**Endpoint:** `POST /api/posts/<id>/comments`

**Parameters:**
- `id` (integer) - ID của bài viết

**Headers:**
- `Content-Type: application/json`
- Cookie với session hợp lệ

**Request Body:**
```json
{
  "content": "Bình luận của tôi..."
}
```

**Response (201):**
```json
{
  "id": 10,
  "message": "Comment added"
}
```

**Error Responses:**
- `401`: Unauthorized
- `400`: Content required

**Example:**
```bash
curl -X POST http://127.0.0.1:5000/api/posts/1/comments \
  -H "Content-Type: application/json" \
  -d '{"content":"Great post!"}' \
  --cookie "session=YOUR_SESSION_COOKIE"
```

---

## 👥 Users Endpoints

### 8. Get All Users
Lấy danh sách user. **Chỉ admin.**

**Endpoint:** `GET /api/users`

**Headers:**
- Cookie với session hợp lệ (admin)

**Response:**
```json
[
  {
    "id": 1,
    "username": "admin",
    "role": "admin",
    "created_at": "2025-11-18 10:00:00"
  },
  {
    "id": 2,
    "username": "user123",
    "role": "user",
    "created_at": "2025-11-18 11:00:00"
  }
]
```

**Error Response (401):**
```json
{
  "error": "Unauthorized"
}
```

**Example:**
```bash
curl http://127.0.0.1:5000/api/users \
  --cookie "session=YOUR_SESSION_COOKIE"
```

---

## 🔐 Authentication Flow

### Bước 1: Đăng nhập qua Web
```bash
curl -X POST http://127.0.0.1:5000/login \
  -d "username=admin&password=admin123" \
  -c cookies.txt
```

### Bước 2: Sử dụng session cookie
```bash
curl http://127.0.0.1:5000/api/posts \
  -b cookies.txt
```

### Hoặc với JavaScript (Browser)
```javascript
// Đăng nhập trước qua web interface, sau đó:
fetch('http://127.0.0.1:5000/api/posts', {
  credentials: 'include' // Tự động gửi cookies
})
.then(res => res.json())
.then(data => console.log(data));
```

---

## 📊 Response Codes

| Code | Meaning |
|------|---------|
| 200  | Success |
| 201  | Created |
| 400  | Bad Request |
| 401  | Unauthorized (chưa đăng nhập) |
| 403  | Forbidden (không có quyền) |
| 404  | Not Found |
| 500  | Internal Server Error |

---

## 🧪 Testing với Python

```python
import requests

# Tạo session
session = requests.Session()

# Đăng nhập
session.post('http://127.0.0.1:5000/login', data={
    'username': 'admin',
    'password': 'admin123'
})

# Lấy posts
response = session.get('http://127.0.0.1:5000/api/posts')
print(response.json())

# Tạo post
response = session.post('http://127.0.0.1:5000/api/posts', json={
    'title': 'New Post',
    'content': 'Content here'
})
print(response.json())

# Thêm comment
response = session.post('http://127.0.0.1:5000/api/posts/1/comments', json={
    'content': 'Nice post!'
})
print(response.json())
```

---

## 🧪 Testing với JavaScript (Node.js)

```javascript
const axios = require('axios');

const api = axios.create({
  baseURL: 'http://127.0.0.1:5000',
  withCredentials: true
});

async function test() {
  // Đăng nhập
  await api.post('/login', new URLSearchParams({
    username: 'admin',
    password: 'admin123'
  }));
  
  // Lấy posts
  const posts = await api.get('/api/posts');
  console.log(posts.data);
  
  // Tạo post
  const newPost = await api.post('/api/posts', {
    title: 'Test',
    content: 'Hello World'
  });
  console.log(newPost.data);
}

test();
```

---

## 💡 Best Practices

1. **Always check authentication:**
   - API yêu cầu session-based auth
   - Đăng nhập trước khi call protected endpoints

2. **Handle errors properly:**
   - Check status codes
   - Parse error messages

3. **Rate limiting:**
   - Không spam requests
   - Implement delay giữa các requests

4. **Content-Type:**
   - Luôn set `Content-Type: application/json` cho POST/PUT

5. **CORS:**
   - Nếu call từ domain khác, cần enable CORS trong Flask

---

## 🔄 Pagination (Future Feature)

Hiện tại API trả về tất cả records. Trong tương lai có thể thêm:

```
GET /api/posts?page=1&limit=10
```

---

## 📝 Notes

- API không hỗ trợ upload ảnh qua JSON (chỉ qua web form)
- Session timeout theo Flask default (permanent=False)
- Không có token-based auth (JWT) - sử dụng session cookies
- HTTPS nên được enable trong production

---

**Last Updated:** 2025-11-18
