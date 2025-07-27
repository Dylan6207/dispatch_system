import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'defaultsecretkey')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///dispatch.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 可選：管理者初始化帳密（用於自動建立 admin 帳號）
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')
