from flask import Blueprint, request, render_template, redirect, url_for, session
from app.models.database import db, User
from app.services.user_service import UserService

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = UserService.authenticate(username, password)
        if user:
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('report.index'))
        return "Login inválido"
    return render_template('login.html')

@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        is_admin = bool(request.form.get('is_admin'))
        UserService.register(username, password, is_admin)
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth_blueprint.route('/logout', methods=['GET'])
def logout():
    session.clear()  
    return redirect(url_for('auth.login')) 
