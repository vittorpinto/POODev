from flask import Flask, render_template, request, send_file
import os
from models import Dataset, Usuario, FormatadorLinguagemNatural, GeradorRelatorioPDF, InsightsNegocio, AnalisadorDados
from tasks import gerar_relatorio_pdf
from rq import Queue
from rq.job import Job  
from redis import Redis
from werkzeug.utils import secure_filename

# Configuração do Redis e RQ
redis_conn = Redis()
fila = Queue(connection=redis_conn)

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Página inicial com o formulário de upload
@app.route('/')
def index():
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

        job = fila.enqueue(gerar_relatorio_pdf, filepath, "Admin")
        
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

if __name__ == "__main__":
    app.run(debug=True, port=5001)
