from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy()
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

from models import User  # 確保這行在 db.init_app 之後
from routes import *

def init_admin_account():
    username = os.environ.get("ADMIN_USERNAME")
    password = os.environ.get("ADMIN_PASSWORD")

    existing_admin = User.query.filter_by(username=username).first()
    if not existing_admin:
        hashed_password = generate_password_hash(password)
        new_admin = User(username=username, password=hashed_password, is_admin=True)
        db.session.add(new_admin)
        db.session.commit()
        print(f"✅ Admin 帳號建立完成：{username}")
    else:
        print("⚠️ 管理員已存在，略過建立")

# 啟動程式
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        init_admin_account()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
