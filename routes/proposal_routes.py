from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Proposal
from flask_login import current_user, login_required

proposal_routes = Blueprint('proposal', __name__)

@proposal_routes.route('/proposals')
@login_required
def list_proposals():
    proposals = Proposal.query.order_by(Proposal.created_at.desc()).all()
    return render_template('proposal_list.html', proposals=proposals)

@proposal_routes.route('/proposals/submit', methods=['GET', 'POST'])
@login_required
def submit_proposal():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        if not title or not content:
            flash('標題與內容皆為必填', 'danger')
            return redirect(url_for('proposal.submit_proposal'))

        new_proposal = Proposal(title=title, content=content, proposer_id=current_user.id)
        db.session.add(new_proposal)
        db.session.commit()
        flash('提案已提交成功', 'success')
        return redirect(url_for('proposal.list_proposals'))

    return render_template('proposal_submit.html')


@proposal_routes.route("/edit/<int:proposal_id>", methods=["GET", "POST"])
@login_required
def edit_proposal(proposal_id):
    if current_user.role != 'admin':
        flash("只有管理者可以編輯提案", "danger")
        return redirect(url_for("proposal.list_proposals"))
    
    proposal = Proposal.query.get_or_404(proposal_id)
    if request.method == "POST":
        proposal.title = request.form["title"]
        proposal.description = request.form["description"]
        db.session.commit()
        flash("提案已更新", "success")
        return redirect(url_for("proposal.list_proposals"))
    
    return render_template("edit_proposal.html", proposal=proposal)

@proposal_routes.route("/delete/<int:proposal_id>", methods=["POST"])
@login_required
def delete_proposal(proposal_id):
    if current_user.role != 'admin':
        flash("只有管理者可以刪除提案", "danger")
        return redirect(url_for("proposal.list_proposals"))
    
    proposal = Proposal.query.get_or_404(proposal_id)
    db.session.delete(proposal)
    db.session.commit()
    flash("提案已刪除", "success")
    return redirect(url_for("proposal.list_proposals"))

