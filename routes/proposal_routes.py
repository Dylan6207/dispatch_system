from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models import Proposal, User
from .. import db

proposal_bp = Blueprint('proposal', __name__, url_prefix='/proposal')

@proposal_bp.route('/list')
@login_required
def list_proposals():
    proposals = Proposal.query.order_by(Proposal.created_at.desc()).all()
    return render_template('proposal_list.html', proposals=proposals)

@proposal_bp.route('/submit', methods=['GET','POST'])
@login_required
def submit_proposal():
    if request.method=='POST':
        title = request.form['title']; description = request.form['description']
        if not title or not description:
            flash('標題與內容皆為必填', 'danger')
        else:
            p = Proposal(title=title, description=description, proposer_id=current_user.id)
            db.session.add(p); db.session.commit()
            flash('提案已提交', 'success')
            return redirect(url_for('proposal.list_proposals'))
    return render_template('proposal_submit.html')

@proposal_bp.route('/claim/<int:pid>', methods=['POST'])
@login_required
def claim_proposal(pid):
    p = Proposal.query.get_or_404(pid)
    if p.claimed_by:
        flash('該案已被搶', 'warning')
    else:
        p.claimed_by = current_user.id
        p.status = 'claimed'
        db.session.commit()
        flash('成功搶案', 'success')
    return redirect(url_for('proposal.list_proposals'))

