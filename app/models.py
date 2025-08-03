from app.extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta, timezone

＃將 UTC 時間轉換為當地時間（In this case ,i built web server in Singapore Render server）
def to_local(dt):
    if dt is None:
        return None
    local_tz = timezone(timedelta(hours=8))
    return dt.astimezone(local_tz)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    county = db.Column(db.String(20), nullable=True)  # 縣市
    town = db.Column(db.String(20), nullable=True)    # 鄉鎮市
    village = db.Column(db.String(20), nullable=True) # 村里

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def local_created_at(self):
        return to_local(self.created_at)

class Bid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    bid_time = db.Column(db.DateTime, default=datetime.utcnow)

def init_admin_account(app):
    with app.app_context():
        admin_username = app.config.get('ADMIN_USERNAME') or 'admin'
        admin_password = app.config.get('ADMIN_PASSWORD') or 'admin'
        admin = User.query.filter_by(username=admin_username).first()
        if not admin:
            admin = User(username=admin_username, is_admin=True)
            admin.set_password(admin_password)
            db.session.add(admin)
            db.session.commit()
        else:
            admin.set_password(admin_password)
            db.session.commit()
