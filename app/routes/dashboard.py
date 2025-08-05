from flask import Blueprint, render_template, redirect, url_for
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

@dashboard_bp.route("/index")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.show_dashboard"))
    # 未登入時顯示公開提案
    proposals = Project.query.with_entities(
        Project.title,
        Project.created_at,
        Project.county,
        Project.town,
        Project.village
    ).limit(20).all()
    return render_template("public_proposals.html", proposals=proposals)
