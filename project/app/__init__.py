from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from redis import Redis
from rq import Queue
import os

db = SQLAlchemy()

# Inicializar a conexão com o Redis
redis_conn = Redis()
fila = Queue('fila', connection=redis_conn)  # Fila para o RQ

def create_app():
    app = Flask(__name__)
    instance_path = os.path.join(app.instance_path, 'site.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{instance_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'sua_chave_secreta'

    db.init_app(app)

    # Importar e registrar blueprints
    from app.controllers.auth_controller import auth_blueprint
    from app.controllers.report_controller import report_blueprint
    from app.controllers.user_controller import user_blueprint

    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(report_blueprint, url_prefix='/')
    app.register_blueprint(user_blueprint, url_prefix='/user')

    return app