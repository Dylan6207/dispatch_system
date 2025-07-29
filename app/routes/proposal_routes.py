
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from ..models import User, Project, Bid
from .. import db

proposal_bp = Blueprint('proposal', __name__, url_prefix='/proposal')

# 新增: 專案競標路由
from flask import Blueprint, request
from flask_login import login_required, current_user
from ..models import Project, Bid
from .. import db

@proposal_bp.route('/projects/<int:project_id>/bid', methods=['POST'])
@login_required
def bid_project(project_id):
    project = Project.query.get_or_404(project_id)
    # 檢查是否已經投過標
    existing_bid = Bid.query.filter_by(user_id=current_user.id, project_id=project_id).first()
    if existing_bid:
        return jsonify({'message': '您已經投過標'}), 400
    bid = Bid(user_id=current_user.id, project_id=project_id)
    db.session.add(bid)
    db.session.commit()
    return jsonify({'message': '競標成功', 'bid_time': bid.bid_time.isoformat()}), 201

@proposal_bp.route('/list')
@login_required
def list_proposals():
    projects = Project.query.order_by(Project.created_at.desc()).all()
    return render_template('proposal_list.html', projects=projects)

@proposal_bp.route('/submit', methods=['GET','POST'])
@login_required
def submit_proposal():
    if request.method=='POST':
        title = request.form['title']; description = request.form['description']
        if not title or not description:
            flash('標題與內容皆為必填', 'danger')
        else:
            project = Project(title=title, description=description)
            db.session.add(project); db.session.commit()
            flash('專案已提交', 'success')
            return redirect(url_for('proposal.list_proposals'))
    return render_template('proposal_submit.html')

# 如需 claim 功能，請根據 Project model 擴充

