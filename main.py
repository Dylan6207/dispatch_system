import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# 初始化 Flask App
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'defaultsecret')

# 設定資料庫
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dispatch.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 初始化登入管理器
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# 使用者模型
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# 登入用 callback
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 首頁
@app.route('/')
def index():
    return render_template('index.html')

# 登入
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.check_password(request.form['password']):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('登入失敗')
    return render_template('login.html')

# 登出
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# 初始化 admin 帳號
def init_admin_account():
    with app.app_context():
        db.create_all()  # 確保資料表已建立

        admin_username = os.environ.get('ADMIN_USERNAME')
        admin_password = os.environ.get('ADMIN_PASSWORD')

        existing_admin = User.query.filter_by(username=admin_username).first()
        if not existing_admin:
            admin_user = User(username=admin_username, is_admin=True)
            admin_user.set_password(admin_password)
            db.session.add(admin_user)
            db.session.commit()
            print(f'✅ 管理員帳號已建立：{admin_username}')
        else:
            print(f'ℹ️ 管理員帳號已存在：{admin_username}')

# 主程式進入點
if __name__ == '__main__':
    init_admin_account()
    app.run(host='0.0.0.0', port=5000)

