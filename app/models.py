from app.extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # 可擴充其他欄位

class Bid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    bid_time = db.Column(db.DateTime, default=datetime.utcnow)
    # 可擴充其他欄位

def init_admin_account(app):
    with app.app_context():
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', is_admin=True)
            admin_password = app.config.get('ADMIN_PASSWORD')
            if not admin_password:
                admin_password = 'admin'
            admin.set_password(admin_password)
            db.session.add(admin)
            db.session.commit()
