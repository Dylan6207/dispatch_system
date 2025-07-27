import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask import render_template

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
login_manager.login_view = 'auth.login'

# 匯入模型與 Blueprint
from models import User  # 確保 models.py 中有定義 User
from routes import auth, proposal_routes, dashboard  # 這些 routes.py 要存在且已設為 blueprint

# 註冊 Blueprint
app.register_blueprint(auth)
app.register_blueprint(proposal_routes)
app.register_blueprint(dashboard)

# 註冊登入管理器的使用者加載函式
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 建立資料庫表格
with app.app_context():
    db.create_all()

# 預設首頁 為 'dashboard.html'
@app.route('/')
def index():
    return render_template('dashboard.html')  # 或其他你寫的首頁html


# 啟動 Flask 應用程式
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
