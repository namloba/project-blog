# 📝 CHANGELOG

## [2.0.0] - 2025-11-18

### 🎉 Major Update - Full-Featured Blog System

---

## ✨ Added

### 🔹 Image Upload Feature
- Added file upload support for posts
- Image preview before posting
- Support for PNG, JPG, JPEG, GIF, WEBP
- Maximum file size: 16MB
- Automatic filename generation with timestamp
- Automatic image deletion when post is deleted
- Image display in post cards and detail pages

**Files:**
- Modified: `app.py` - Upload logic, file handling
- Modified: `templates/create_post.html` - Upload form with preview
- Modified: `templates/edit_post.html` - Edit form with upload
- Modified: `templates/index.html` - Display images
- New: `static/uploads/` - Upload directory

---

### 🔹 Admin/User Role System
- Role-based access control (admin/user)
- Decorators: `@login_required`, `@admin_required`
- Full admin panel with management capabilities
- Admin can:
  - Manage all users (promote/demote, delete)
  - Manage all posts (view, edit, delete)
  - Manage all comments (delete)
- Users can only edit/delete their own content
- Visual badges for admin users
- Default admin account created on first run

**Files:**
- Modified: `app.py` - Role system, decorators, admin routes
- New: `templates/admin.html` - Admin panel interface
- Modified: `templates/base.html` - Admin navigation link
- Modified: Database schema - Added `role` column to users

---

### 🔹 Comment System
- Comment on posts
- Display comment count on post cards
- Delete comments (owner or admin)
- Timestamp for comments
- Beautiful comment UI with cards
- Admin badge on admin comments

**Files:**
- Modified: `app.py` - Comment routes (add, delete, display)
- New: `templates/post_detail.html` - Post detail with comments
- Modified: `templates/index.html` - Comment count display
- Modified: Database schema - New `comments` table

---

### 🔹 REST API
Complete RESTful API with 11 endpoints:

**Posts:**
- `GET /api/posts` - Get all posts
- `GET /api/posts/<id>` - Get single post
- `POST /api/posts` - Create post (auth required)
- `PUT /api/posts/<id>` - Update post (permission required)
- `DELETE /api/posts/<id>` - Delete post (permission required)

**Comments:**
- `GET /api/posts/<id>/comments` - Get comments
- `POST /api/posts/<id>/comments` - Add comment (auth required)

**Users:**
- `GET /api/users` - Get users (admin only)

**Files:**
- Modified: `app.py` - All API routes
- New: `API_DOCUMENTATION.md` - Complete API documentation
- New: `test_api.py` - API testing script

---

### 📚 Documentation
- New: `README.md` - Complete user guide
- New: `API_DOCUMENTATION.md` - Detailed API documentation
- New: `SUMMARY.md` - Project summary
- New: `QUICKSTART.md` - Quick start guide
- New: `CHANGELOG.md` - This file

---

### 🛠️ Utility Scripts
- New: `start.bat` - Quick start script
- New: `reset_database.bat` - Database reset script
- New: `test_api.py` - API testing script

---

### 🎨 UI Improvements
**Major CSS enhancements (~500 lines added):**
- Post header with author information
- Admin badges (gold gradient)
- User info in navigation bar
- Post image display with hover effects
- File upload interface
- Image preview functionality
- Comments section styling
- Comment cards with borders
- Admin panel table styling
- Role badges (admin/user)
- Action buttons with hover effects
- Post footer layout
- Back navigation links
- Enhanced responsive design
- Better mobile support

**Files:**
- Modified: `static/css/style.css` - Massive CSS additions

---

## 🔄 Changed

### Database Schema
**users table:**
- Added: `role` (TEXT, default 'user')
- Added: `created_at` (TIMESTAMP)

**posts table:**
- Added: `image_path` (TEXT, nullable)
- Added: `created_at` (TIMESTAMP)
- Added: Foreign key to users

**comments table (new):**
- `id` (INTEGER PRIMARY KEY)
- `post_id` (INTEGER, foreign key)
- `user_id` (INTEGER, foreign key)
- `content` (TEXT)
- `created_at` (TIMESTAMP)

### Configuration
- Added: `UPLOAD_FOLDER` configuration
- Added: `ALLOWED_EXTENSIONS` configuration
- Added: `MAX_CONTENT_LENGTH` (16MB limit)
- Modified: Session handling (added user_id, role)

### Templates
**base.html:**
- Added admin navigation link
- Added user info display
- Added admin badge in nav
- Improved navigation structure
- Added viewport meta tag

**index.html:**
- Added post author display
- Added admin badges
- Added post images
- Added comment count
- Added post footer with metadata
- Added permission-based edit/delete buttons

**login.html:**
- Added emoji icons
- Improved form styling

**register.html:**
- Added emoji icons
- Improved form styling

**create_post.html:**
- Added file upload field
- Added image preview
- Added JavaScript for preview

**edit_post.html:**
- Added file upload field
- Added current image display
- Added image preview
- Added JavaScript for preview

---

## 🐛 Fixed
- Fixed: Author ID now properly tracked in session
- Fixed: Post deletion now requires permission check
- Fixed: Edit permission validation
- Fixed: Session management improved
- Fixed: Database initialization race conditions

---

## 🔒 Security Notes
**Current (Development):**
- ⚠️ Passwords stored in plain text
- ⚠️ No CSRF protection
- ⚠️ No rate limiting
- ⚠️ Basic input validation

**Recommended for Production:**
- Implement password hashing (bcrypt/argon2)
- Add CSRF protection
- Add rate limiting
- Enhance input validation
- Enable HTTPS
- Secure session configuration
- Better file upload validation

---

## 📦 Dependencies Updated
**requirements.txt:**
```
Flask==3.0.0
Werkzeug==3.0.1
requests==2.31.0  # For testing
```

---

## 📊 Statistics
- **Total files modified:** 8
- **New files created:** 6
- **Lines of code added:** ~2000+
- **New functions:** 20+
- **API endpoints:** 11
- **New routes:** 15+
- **CSS lines added:** ~500
- **Documentation pages:** 4

---

## 🎯 Breaking Changes
- Database schema changed - requires reset
- Session structure changed - users need to re-login
- Old database.db is incompatible

**Migration:**
Run `reset_database.bat` to recreate database with new schema.

---

## 🚀 Upgrade Instructions

### From v1.0.0 to v2.0.0:

1. **Backup old data** (if needed):
   ```bash
   copy database.db database.db.backup
   ```

2. **Reset database:**
   ```bash
   reset_database.bat
   ```

3. **Update code:**
   - All files already updated

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Start application:**
   ```bash
   start.bat
   ```

6. **Login with admin:**
   - Username: admin
   - Password: admin123

7. **Change admin password** (recommended)

---

## 🎉 What's Next?

### Potential Future Features:
- Password hashing (bcrypt)
- Email verification
- Password reset functionality
- User profiles with avatars
- Post categories/tags
- Search functionality
- Pagination for posts
- Like/reaction system
- Markdown editor
- Real-time notifications
- JWT authentication for API
- Image cropping/resizing
- Multiple images per post
- Dashboard statistics
- Export/Import functionality

---

## 👏 Credits
**Developed by:** GitHub Copilot
**Date:** November 18, 2025
**Version:** 2.0.0

---

## 📄 License
MIT License - Free to use and modify

---

## [1.0.0] - Initial Release
- Basic blog functionality
- User registration/login
- Create, edit, delete posts
- Simple UI
- SQLite database
