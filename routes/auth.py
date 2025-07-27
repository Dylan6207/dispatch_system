from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import User
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard.show_dashboard'))
        else:
            flash('帳號或密碼錯誤', 'danger')
            return redirect(url_for('auth.login'))
    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('你已登出', 'success')
    return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # 註冊邏輯
        pass
    return render_template('register.html')
