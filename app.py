from flask import Flask, render_template, request, redirect, session, jsonify, url_for
from werkzeug.utils import secure_filename
from functools import wraps
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secret-key-change-in-production"

# Configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create upload folder if not exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    db = get_db()
    # Users table with role (admin/user)
    db.execute("""CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        username TEXT UNIQUE, 
        password TEXT,
        role TEXT DEFAULT 'user',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );""")
    
    # Posts table with image support
    db.execute("""CREATE TABLE IF NOT EXISTS posts(
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        title TEXT, 
        content TEXT, 
        author_id INTEGER,
        image_path TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(author_id) REFERENCES users(id)
    );""")
    
    # Comments table
    db.execute("""CREATE TABLE IF NOT EXISTS comments(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        post_id INTEGER,
        user_id INTEGER,
        content TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(post_id) REFERENCES posts(id) ON DELETE CASCADE,
        FOREIGN KEY(user_id) REFERENCES users(id)
    );""")
    
    db.commit()
    
    # Create default admin if not exists
    admin = db.execute("SELECT * FROM users WHERE username='admin'").fetchone()
    if not admin:
        db.execute("INSERT INTO users(username, password, role) VALUES (?, ?, ?)", 
                  ('admin', 'admin123', 'admin'))
        db.commit()

init_db()

# Decorators
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect('/login')
        db = get_db()
        user = db.execute("SELECT role FROM users WHERE id=?", (session['user_id'],)).fetchone()
        if not user or user['role'] != 'admin':
            return "Access Denied: Admin only!", 403
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
def home():
    db = get_db()
    posts = db.execute("""
        SELECT posts.*, users.username, users.role
        FROM posts 
        LEFT JOIN users ON posts.author_id = users.id 
        ORDER BY posts.id DESC
    """).fetchall()
    
    # Get comment counts for each post
    posts_with_counts = []
    for post in posts:
        comment_count = db.execute("SELECT COUNT(*) as count FROM comments WHERE post_id=?", 
                                   (post['id'],)).fetchone()['count']
        posts_with_counts.append({
            'id': post['id'],
            'title': post['title'],
            'content': post['content'],
            'image_path': post['image_path'],
            'username': post['username'],
            'role': post['role'],
            'created_at': post['created_at'],
            'comment_count': comment_count
        })
    
    return render_template("index.html", posts=posts_with_counts)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        pw = request.form["password"]
        db = get_db()
        result = db.execute("SELECT * FROM users WHERE username=? AND password=?", (user, pw)).fetchone()
        if result:
            session["user"] = user
            session["user_id"] = result['id']
            session["role"] = result['role']
            return redirect("/")
        return "Sai thông tin đăng nhập!"
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = request.form["username"]
        pw = request.form["password"]
        db = get_db()
        try:
            db.execute("INSERT INTO users(username, password) VALUES (?, ?)", (user, pw))
            db.commit()
            return redirect("/login")
        except:
            return "User đã tồn tại!"
    return render_template("register.html")

@app.route("/create", methods=["GET", "POST"])
@login_required
def create_post():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        image_path = None
        
        # Handle image upload
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Add timestamp to avoid filename conflicts
                filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_path = f"uploads/{filename}"
        
        db = get_db()
        db.execute("INSERT INTO posts(title, content, author_id, image_path) VALUES (?, ?, ?, ?)", 
                  (title, content, session['user_id'], image_path))
        db.commit()
        return redirect("/")
    return render_template("create_post.html")

@app.route("/edit/<id>", methods=["GET", "POST"])
@login_required
def edit_post(id):
    db = get_db()
    post = db.execute("SELECT * FROM posts WHERE id=?", (id,)).fetchone()
    
    # Check if user is author or admin
    if post['author_id'] != session['user_id'] and session.get('role') != 'admin':
        return "Unauthorized!", 403
    
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        image_path = post['image_path']
        
        # Handle new image upload
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                # Delete old image if exists
                if image_path:
                    old_path = os.path.join('static', image_path)
                    if os.path.exists(old_path):
                        os.remove(old_path)
                
                filename = secure_filename(file.filename)
                filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_path = f"uploads/{filename}"
        
        db.execute("UPDATE posts SET title=?, content=?, image_path=? WHERE id=?", 
                  (title, content, image_path, id))
        db.commit()
        return redirect("/")
    return render_template("edit_post.html", post=post)

@app.route("/delete/<id>")
@login_required
def delete_post(id):
    db = get_db()
    post = db.execute("SELECT * FROM posts WHERE id=?", (id,)).fetchone()
    
    # Check if user is author or admin
    if post['author_id'] != session['user_id'] and session.get('role') != 'admin':
        return "Unauthorized!", 403
    
    # Delete image if exists
    if post['image_path']:
        image_full_path = os.path.join('static', post['image_path'])
        if os.path.exists(image_full_path):
            os.remove(image_full_path)
    
    db.execute("DELETE FROM posts WHERE id=?", (id,))
    db.commit()
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/about")
def about():
    return render_template("about.html")

# Post detail with comments
@app.route("/post/<int:id>")
def post_detail(id):
    db = get_db()
    post = db.execute("""
        SELECT posts.*, users.username, users.role
        FROM posts 
        LEFT JOIN users ON posts.author_id = users.id 
        WHERE posts.id=?
    """, (id,)).fetchone()
    
    if not post:
        return "Post not found!", 404
    
    # Get comments for this post
    comments = db.execute("""
        SELECT comments.*, users.username, users.role
        FROM comments
        LEFT JOIN users ON comments.user_id = users.id
        WHERE comments.post_id=?
        ORDER BY comments.created_at DESC
    """, (id,)).fetchall()
    
    return render_template("post_detail.html", post=post, comments=comments)

# Add comment
@app.route("/post/<int:id>/comment", methods=["POST"])
@login_required
def add_comment(id):
    content = request.form.get("content")
    if content:
        db = get_db()
        db.execute("INSERT INTO comments(post_id, user_id, content) VALUES (?, ?, ?)",
                  (id, session['user_id'], content))
        db.commit()
    return redirect(f"/post/{id}")

# Delete comment
@app.route("/comment/<int:id>/delete")
@login_required
def delete_comment(id):
    db = get_db()
    comment = db.execute("SELECT * FROM comments WHERE id=?", (id,)).fetchone()
    
    if not comment:
        return "Comment not found!", 404
    
    # Check if user is comment owner or admin
    if comment['user_id'] != session['user_id'] and session.get('role') != 'admin':
        return "Unauthorized!", 403
    
    post_id = comment['post_id']
    db.execute("DELETE FROM comments WHERE id=?", (id,))
    db.commit()
    return redirect(f"/post/{post_id}")

# Admin panel
@app.route("/admin")
@admin_required
def admin_panel():
    db = get_db()
    users = db.execute("SELECT * FROM users ORDER BY id DESC").fetchall()
    all_posts = db.execute("""
        SELECT posts.*, users.username 
        FROM posts 
        LEFT JOIN users ON posts.author_id = users.id 
        ORDER BY posts.id DESC
    """).fetchall()
    all_comments = db.execute("""
        SELECT comments.*, users.username, posts.title as post_title
        FROM comments
        LEFT JOIN users ON comments.user_id = users.id
        LEFT JOIN posts ON comments.post_id = posts.id
        ORDER BY comments.id DESC
    """).fetchall()
    
    return render_template("admin.html", users=users, posts=all_posts, comments=all_comments)

# Admin: Toggle user role
@app.route("/admin/user/<int:id>/toggle_role")
@admin_required
def toggle_user_role(id):
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE id=?", (id,)).fetchone()
    if user:
        new_role = 'admin' if user['role'] == 'user' else 'user'
        db.execute("UPDATE users SET role=? WHERE id=?", (new_role, id))
        db.commit()
    return redirect("/admin")

# Admin: Delete user
@app.route("/admin/user/<int:id>/delete")
@admin_required
def admin_delete_user(id):
    if id == session['user_id']:
        return "Cannot delete yourself!", 403
    db = get_db()
    db.execute("DELETE FROM users WHERE id=?", (id,))
    db.commit()
    return redirect("/admin")

# ============= API ROUTES =============

# API: Get all posts
@app.route("/api/posts", methods=["GET"])
def api_get_posts():
    db = get_db()
    posts = db.execute("""
        SELECT posts.*, users.username
        FROM posts 
        LEFT JOIN users ON posts.author_id = users.id 
        ORDER BY posts.id DESC
    """).fetchall()
    return jsonify([dict(post) for post in posts])

# API: Get single post
@app.route("/api/posts/<int:id>", methods=["GET"])
def api_get_post(id):
    db = get_db()
    post = db.execute("""
        SELECT posts.*, users.username
        FROM posts 
        LEFT JOIN users ON posts.author_id = users.id 
        WHERE posts.id=?
    """, (id,)).fetchone()
    if not post:
        return jsonify({"error": "Post not found"}), 404
    return jsonify(dict(post))

# API: Create post (requires authentication)
@app.route("/api/posts", methods=["POST"])
def api_create_post():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    data = request.get_json()
    if not data or 'title' not in data or 'content' not in data:
        return jsonify({"error": "Title and content required"}), 400
    
    db = get_db()
    cursor = db.execute("INSERT INTO posts(title, content, author_id) VALUES (?, ?, ?)",
                       (data['title'], data['content'], session['user_id']))
    db.commit()
    
    return jsonify({"id": cursor.lastrowid, "message": "Post created"}), 201

# API: Update post
@app.route("/api/posts/<int:id>", methods=["PUT"])
def api_update_post(id):
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    db = get_db()
    post = db.execute("SELECT * FROM posts WHERE id=?", (id,)).fetchone()
    if not post:
        return jsonify({"error": "Post not found"}), 404
    
    if post['author_id'] != session['user_id'] and session.get('role') != 'admin':
        return jsonify({"error": "Forbidden"}), 403
    
    data = request.get_json()
    title = data.get('title', post['title'])
    content = data.get('content', post['content'])
    
    db.execute("UPDATE posts SET title=?, content=? WHERE id=?", (title, content, id))
    db.commit()
    
    return jsonify({"message": "Post updated"})

# API: Delete post
@app.route("/api/posts/<int:id>", methods=["DELETE"])
def api_delete_post(id):
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    db = get_db()
    post = db.execute("SELECT * FROM posts WHERE id=?", (id,)).fetchone()
    if not post:
        return jsonify({"error": "Post not found"}), 404
    
    if post['author_id'] != session['user_id'] and session.get('role') != 'admin':
        return jsonify({"error": "Forbidden"}), 403
    
    db.execute("DELETE FROM posts WHERE id=?", (id,))
    db.commit()
    
    return jsonify({"message": "Post deleted"})

# API: Get comments for a post
@app.route("/api/posts/<int:id>/comments", methods=["GET"])
def api_get_comments(id):
    db = get_db()
    comments = db.execute("""
        SELECT comments.*, users.username
        FROM comments
        LEFT JOIN users ON comments.user_id = users.id
        WHERE comments.post_id=?
        ORDER BY comments.created_at DESC
    """, (id,)).fetchall()
    return jsonify([dict(comment) for comment in comments])

# API: Add comment
@app.route("/api/posts/<int:id>/comments", methods=["POST"])
def api_add_comment(id):
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    data = request.get_json()
    if not data or 'content' not in data:
        return jsonify({"error": "Content required"}), 400
    
    db = get_db()
    cursor = db.execute("INSERT INTO comments(post_id, user_id, content) VALUES (?, ?, ?)",
                       (id, session['user_id'], data['content']))
    db.commit()
    
    return jsonify({"id": cursor.lastrowid, "message": "Comment added"}), 201

# API: Get all users (admin only)
@app.route("/api/users", methods=["GET"])
def api_get_users():
    if 'user_id' not in session or session.get('role') != 'admin':
        return jsonify({"error": "Unauthorized"}), 401
    
    db = get_db()
    users = db.execute("SELECT id, username, role, created_at FROM users").fetchall()
    return jsonify([dict(user) for user in users])

if __name__ == "__main__":
    app.run(debug=True)
