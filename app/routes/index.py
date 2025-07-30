from flask import Blueprint, render_template, redirect, url_for, request

index_bp = Blueprint('index', __name__)

@index_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return redirect(url_for('auth.login'))
    return render_template('login.html')
