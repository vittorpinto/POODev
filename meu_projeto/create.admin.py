from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    db.create_all() 
    admin = User(username='admin', password='securepassword', is_admin=True)
    db.session.add(admin)
    db.session.commit()
    print("Usuário administrador criado com sucesso!")
    print(f"Banco de dados em uso: {app.config['SQLALCHEMY_DATABASE_URI']}")
