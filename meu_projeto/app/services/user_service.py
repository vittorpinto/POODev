from app.models.database import db, User

class UserService:
    @staticmethod
    def authenticate(username, password):
        """
        Autentica o usuário com base no nome de usuário e senha.
        """
        return User.query.filter_by(username=username, password=password).first()

    @staticmethod
    def register(username, password, is_admin=False):
        """
        Registra um novo usuário.
        """
        user = User(username=username, password=password, is_admin=is_admin)
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def is_admin(user_id):
        """
        Verifica se o usuário é administrador.
        """
        user = User.query.filter_by(id=user_id).first()
        return user.is_admin if user else False
