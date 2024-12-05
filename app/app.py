from flask import Flask, render_template, request, send_file, session, redirect, url_for
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
import os
from redis import Redis
from rq import Queue
from rq.job import Job

from database import db, User, Report
from models import Dataset, Usuario, FormatadorLinguagemNatural, GeradorRelatorioPDF, InsightsNegocio, AnalisadorDados
from tasks import gerar_relatorio_pdf

# Inicialização do Flask
app = Flask(__name__)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'sua_chave_secreta'

# Configuração de upload
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Configuração do Redis e RQ
redis_conn = Redis()
fila = Queue('fila', connection=redis_conn)

# Inicializar o SQLAlchemy com o app
db.init_app(app)

# Criar tabelas no banco de dados (se necessário)
with app.app_context():
    db.create_all()

# Página inicial com o formulário de upload
@app.route('/')
def index():
    if 'user_id' in session:
        print(f"Usuário logado: {session['username']} (ID: {session['user_id']})")
    return render_template('index.html')

# Rota para processar o upload e gerar o relatório
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "Nenhum arquivo selecionado!"
    
    file = request.files['file']
    
    if file.filename == '':
        return "Nenhum arquivo selecionado!"
    
    if file and file.filename.endswith('.csv'):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Enfileirar tarefa com o user_id logado
        job = fila.enqueue(
            gerar_relatorio_pdf,
            filepath,
            session['username'],  # Nome do usuário
            session['user_id'],   # ID do usuário logado
            app.config['SQLALCHEMY_DATABASE_URI']
        )
        
        return f"""
            <h3>Tarefa enfileirada com sucesso!</h3>
            <p>ID da Tarefa: {job.get_id()}</p>
            <p><a href="/status/{job.get_id()}">Clique aqui para verificar o status da tarefa</a></p>
        """
    else:
        return "Arquivo inválido! Por favor, faça upload de um arquivo CSV."

# Rota para verificar o status da tarefa
@app.route('/status/<job_id>', methods=['GET'])
def job_status(job_id):
    job = Job.fetch(job_id, connection=redis_conn)
    
    if job.is_finished:
        return f"O relatório está pronto! <a href='/download/{job.result}'>Clique aqui para baixar o relatório</a>."
    elif job.is_queued:
        return "O relatório está na fila para ser gerado."
    elif job.is_started:
        return "O relatório está sendo gerado."
    elif job.is_failed:
        return "Houve um erro na geração do relatório."
    else:
        return "Status desconhecido."

# Rota para download do PDF
@app.route('/download/<path:filename>', methods=['GET'])
def download_file(filename):
    return send_file(filename, as_attachment=True)

@app.route('/get_reports', methods=['GET'])
def get_reports():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    reports = Report.query.filter_by(user_id=user_id).all()  # Relatórios do usuário logado

    reports_list = [{"id": r.id, "filename": r.filename} for r in reports]
    return {"reports": reports_list}, 200



# Rota para registrar um usuário
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Converter o valor de 'is_admin' para booleano
        is_admin = True if request.form.get('is_admin') == 'on' else False

        # Criar o usuário
        new_user = User(username=username, password=password, is_admin=is_admin)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))
    return render_template('register.html')


# Rota para login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id
            session['username'] = user.username  # Salva o nome do usuário na sessão
            session['is_admin'] = user.is_admin
            return redirect(url_for('index'))
        else:
            return "Login inválido"
    return render_template('login.html')

# Rota para logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True, port=5001)