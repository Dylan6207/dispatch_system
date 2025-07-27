from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.config import Config
from app.models import db, init_admin_account
from app.routes import auth, users, cases, dashboard

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        db.create_all()
        init_admin_account()

    app.register_blueprint(auth)
    app.register_blueprint(users)
    app.register_blueprint(cases)
    app.register_blueprint(dashboard)

    return app
