from app import app
from database import db, User

# Garante que estamos dentro do contexto do aplicativo Flask
with app.app_context():
    # Verifica se o usuário Admin já existe
    admin_user = User.query.filter_by(username="Admin").first()
    if not admin_user:
        # Cria o usuário Admin
        new_user = User(username="Admin", password="adminpassword", is_admin=True)
        db.session.add(new_user)
        db.session.commit()
        print("Usuário Admin criado com sucesso.")
    else:
        print("Usuário Admin já existe.")
