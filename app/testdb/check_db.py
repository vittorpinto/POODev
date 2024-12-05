from app import app
from database import db, User

# Garante que estamos dentro do contexto do aplicativo
with app.app_context():
    # Consulta para verificar se o usuário "Admin" existe
    user = User.query.filter_by(username="Admin").first()
    if user:
        print(f"Usuário encontrado: {user.username}")
    else:
        print("Usuário não encontrado.")