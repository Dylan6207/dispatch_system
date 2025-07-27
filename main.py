import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.security import generate_password_hash, check_password_hash

# 初始化 Flask App
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'defaultsecret')

# 設定資料庫
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dispatch.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 登入管理器
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

# 匯入模型
from models import User  # 確保你把 User 搬到 models.py
# 或是你還沒搬，可以暫時保留定義在這邊

# 登入用 callback
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 首頁
@app.route('/')
def index():
    return render_template('index.html')

# 初始化管理者帳號
def init_admin_account():
    with app.app_context():
        db.create_all()

        admin_username = os.environ.get('ADMIN_USERNAME')
        admin_password = os.environ.get('ADMIN_PASSWORD')

        if not admin_username or not admin_password:
            print("❌ 請設定 ADMIN_USERNAME 和 ADMIN_PASSWORD 環境變數")
            return

        existing_admin = User.query.filter_by(username=admin_username).first()
        if not existing_admin:
            admin_user = User(username=admin_username, role='admin')
            admin_user.set_password(admin_password)
            db.session.add(admin_user)
            db.session.commit()
            print(f'✅ 管理員帳號已建立：{admin_username}')
        else:
            print(f'ℹ️ 管理員帳號已存在：{admin_username}')

# 匯入與註冊 Blueprint
from routes.auth import auth
from routes.dashboard import dashboard
from routes.proposal_routes import proposal_routes

app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(dashboard, url_prefix='/dashboard')
app.register_blueprint(proposal_routes, url_prefix='/proposals')

# 主程式進入點
if __name__ == '__main__':
    init_admin_account()
    app.run(host='0.0.0.0', port=5000)
