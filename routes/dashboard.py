from flask import Blueprint, render_template
from models import db, Proposal, User
from flask_login import login_required

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/dashboard')
@login_required
def show_dashboard():
    # 可以根據使用者角色分不同儀表板
    all_proposals = Proposal.query.all()
    proposal_count = Proposal.query.count()
    user_count = User.query.count()

    return render_template('dashboard.html',
                           proposal_count=proposal_count,
                           user_count=user_count,
                           proposals=all_proposals)
