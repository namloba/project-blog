"""
Test script để demo các API endpoints
"""
import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def print_response(response, title):
    """Print formatted response"""
    print(f"\n{'='*60}")
    print(f"🔹 {title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2, ensure_ascii=False)}")
    except:
        print(f"Response: {response.text}")

def test_api():
    """Test all API endpoints"""
    session = requests.Session()
    
    print("\n🚀 Bắt đầu test API endpoints...\n")
    
    # 1. Login
    print("1️⃣ Đăng nhập với admin...")
    response = session.post(f"{BASE_URL}/login", data={
        'username': 'admin',
        'password': 'admin123'
    })
    if response.status_code == 200 and "Trang chủ" in response.text:
        print("✅ Đăng nhập thành công!")
    else:
        print("❌ Đăng nhập thất bại!")
        return
    
    # 2. Get all posts
    response = session.get(f"{BASE_URL}/api/posts")
    print_response(response, "GET /api/posts - Lấy tất cả bài viết")
    
    # 3. Create new post
    response = session.post(f"{BASE_URL}/api/posts", 
                          json={
                              'title': 'Bài viết test từ API',
                              'content': 'Đây là nội dung test từ Python script'
                          })
    print_response(response, "POST /api/posts - Tạo bài viết mới")
    
    if response.status_code == 201:
        new_post_id = response.json()['id']
        
        # 4. Get single post
        response = session.get(f"{BASE_URL}/api/posts/{new_post_id}")
        print_response(response, f"GET /api/posts/{new_post_id} - Lấy 1 bài viết")
        
        # 5. Update post
        response = session.put(f"{BASE_URL}/api/posts/{new_post_id}",
                             json={
                                 'title': 'Bài viết đã cập nhật',
                                 'content': 'Nội dung đã được cập nhật qua API'
                             })
        print_response(response, f"PUT /api/posts/{new_post_id} - Cập nhật bài viết")
        
        # 6. Add comment
        response = session.post(f"{BASE_URL}/api/posts/{new_post_id}/comments",
                              json={'content': 'Comment test từ API!'})
        print_response(response, f"POST /api/posts/{new_post_id}/comments - Thêm comment")
        
        # 7. Get comments
        response = session.get(f"{BASE_URL}/api/posts/{new_post_id}/comments")
        print_response(response, f"GET /api/posts/{new_post_id}/comments - Lấy comments")
        
        # 8. Get users (admin only)
        response = session.get(f"{BASE_URL}/api/users")
        print_response(response, "GET /api/users - Lấy danh sách users (admin only)")
        
        # 9. Delete post
        response = session.delete(f"{BASE_URL}/api/posts/{new_post_id}")
        print_response(response, f"DELETE /api/posts/{new_post_id} - Xóa bài viết")
    
    print("\n" + "="*60)
    print("✅ Hoàn tất test API!")
    print("="*60)

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("\n❌ Lỗi: Không thể kết nối đến server!")
        print("Hãy chắc chắn rằng Flask app đang chạy tại http://127.0.0.1:5000")
    except Exception as e:
        print(f"\n❌ Lỗi: {str(e)}")
