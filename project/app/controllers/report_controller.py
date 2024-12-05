from flask import Blueprint, request, render_template, session, redirect, url_for, send_from_directory, abort
from werkzeug.utils import secure_filename
from app.services.report_service import ReportService
import os

report_blueprint = Blueprint('report', __name__)

@report_blueprint.route('/', methods=['GET'])
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('index.html')

@report_blueprint.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "Nenhum arquivo selecionado!"
    
    file = request.files['file']
    if file.filename == '':
        return "Nenhum arquivo selecionado!"

    if file and file.filename.endswith('.csv'):
        filename = secure_filename(file.filename)
        filepath = ReportService.save_file(file, filename)

        job_id = ReportService.enqueue_report(filepath, session['user_id'])
        return f"Tarefa enfileirada com sucesso! ID da Tarefa: {job_id}"
    return "Arquivo inválido!"

@report_blueprint.route('/status/<job_id>', methods=['GET'])
def check_status(job_id):
    status, result = ReportService.check_job_status(job_id)
    if status == "Concluído":
        filename = result.split('/')[-1]
        return f"Relatório gerado com sucesso! <a href='/download/{filename}'>Clique aqui para baixar</a>"
    elif status == "Falhou":
        return "A geração do relatório falhou. Tente novamente."
    elif status == "Em andamento":
        return "A tarefa está em andamento. Aguarde..."
    else:
        return "Job não encontrado."

@report_blueprint.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
    try:
        return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)
    except FileNotFoundError:
        abort(404, description="Arquivo não encontrado")
        
@report_blueprint.route('/get_reports', methods=['GET'])
def get_reports():
    if 'user_id' not in session:
        return {"error": "Usuário não autenticado"}, 401

    user_id = session['user_id']
    
    from app.services.user_service import UserService

    if UserService.is_admin(user_id):
        # Administradores veem todos os relatórios
        reports = ReportService.get_all_reports_with_users()
    else:
        # Usuários veem apenas seus próprios relatórios
        reports = ReportService.get_reports_for_user_with_users(user_id)

    return {"reports": reports}, 200
