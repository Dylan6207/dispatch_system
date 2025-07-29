from flask import Flask
from app.extensions import db, login_manager

from app.models import init_admin_account
from app.routes.auth import auth as auth_bp
from app.routes.dashboard import dashboard_bp
from app.routes.proposal_routes import proposal_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(proposal_bp)

    with app.app_context():
        db.create_all()
        init_admin_account(app)

    return app
