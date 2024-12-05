from flask import Blueprint, render_template, session, redirect, url_for
from app.services.user_service import UserService

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/profile', methods=['GET'])
def profile():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    user = UserService.get_user_by_id(session['user_id'])
    return render_template('profile.html', user=user)
