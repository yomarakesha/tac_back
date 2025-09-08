from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from ..models import db, AdminUser

# Blueprint для аутентификации
auth_bp = Blueprint('auth', __name__)

# Главная страница blueprint — редирект на login
@auth_bp.route('/')
def index():
    return redirect(url_for('auth.login'))

# Login
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = AdminUser.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('admin.index'))  # Перенаправление в админку
        flash('Неверный логин или пароль')
    return render_template('login.html')

# Logout
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))