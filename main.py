import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
from models import User  # 確保 models.py 有 User 定義

# 初始化 Flask app
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "default_demo_secret")

# 設定資料庫
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 初始化 LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# 匯入並註冊 Blueprint（routes）
from routes import auth, proposal_routes, dashboard
app.register_blueprint(auth)
app.register_blueprint(proposal_routes)
app.register_blueprint(dashboard)

# 使用者載入函式
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 自動建立管理者帳號（僅限第一次啟動）
def init_admin_account():
    username = os.getenv("ADMIN_USERNAME")
    password = os.getenv("ADMIN_PASSWORD")

    if not username or not password:
        print("[✘] 環境變數 ADMIN_USERNAME 或 ADMIN_PASSWORD 未設定，略過 admin 建立。")
        return

    existing_admin = User.query.filter_by(username=username).first()
    if existing_admin:
        print(f"[✓] 管理者帳號 '{username}' 已存在，略過建立。")
        return

    new_admin = User(username=username, role="admin")
    new_admin.set_password(password)
    db.session.add(new_admin)
    db.session.commit()
    print(f"[✓] 已成功建立管理者帳號: '{username}'")

# 建立資料表 + 初始化 admin
with app.app_context():
    db.create_all()
    init_admin_account()

# 預設首頁
@app.route('/')
def index():
    return render_template('dashboard.html')

# 啟動應用
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
