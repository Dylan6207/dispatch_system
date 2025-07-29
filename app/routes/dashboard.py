from flask import Blueprint, render_template
from flask_login import login_required, current_user
from ..models import Project, User

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/')
@login_required
def show_dashboard():
    total = Project.query.count()
    allp = Project.query.order_by(Project.created_at.desc()).limit(10).all()
    users = User.query.count()
    return render_template('dashboard.html',
                           proposal_count=total, user_count=users, proposals=allp)
