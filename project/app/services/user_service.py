from app.models.database import db, User

class UserService:
    @staticmethod
    def authenticate(username, password):
        return User.query.filter_by(username=username, password=password).first()

    @staticmethod
    def register(username, password, is_admin=False):
        user = User(username=username, password=password, is_admin=is_admin)
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def is_admin(user_id):
        user = User.query.filter_by(id=user_id).first()
        return user.is_admin if user else False
