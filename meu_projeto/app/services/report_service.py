from app.models.database import db, Report, User  # Certifique-se de importar User

class ReportService:
    @staticmethod
    def save_file(file, filename):
        """
        Salva o arquivo no diretório de uploads.
        """
        UPLOAD_FOLDER = 'uploads'
        filepath = f"{UPLOAD_FOLDER}/{filename}"
        file.save(filepath)
        return filepath

    @staticmethod
    def enqueue_report(filepath, user_id):
        """
        Enfileira uma tarefa para gerar um relatório.
        """
        from app import fila  # Importa a fila de tarefas
        job = fila.enqueue('app.tasks.generate_report', filepath, user_id)
        return job.id

    @staticmethod
    def check_job_status(job_id):
        """
        Verifica o status de uma tarefa de relatório.
        """
        from rq.job import Job
        from app import redis_conn
        job = Job.fetch(job_id, connection=redis_conn)
        if job.is_finished:
            return "Concluído", job.result
        elif job.is_failed:
            return "Falhou", None
        elif job.is_started or job.is_queued:
            return "Em andamento", None
        return "Desconhecido", None

    @staticmethod
    def get_reports_for_user(user_id):
        """
        Retorna todos os relatórios associados ao usuário.
        """
        reports = Report.query.filter_by(user_id=user_id).all()
        return [{
            "id": report.id,
            "filename": report.filename,
            "user_id": report.user_id
        } for report in reports]

    @staticmethod
    def get_reports_for_user_with_users(user_id):
        """
        Retorna os relatórios associados a um usuário, incluindo o nome do criador.
        """
        reports = Report.query.filter_by(user_id=user_id).all()
        return [{
            "id": report.id,
            "filename": report.filename,
            "user_id": report.user_id,
            "username": User.query.filter_by(id=report.user_id).first().username
        } for report in reports]

    @staticmethod
    def get_all_reports_with_users():
        """
        Retorna todos os relatórios no sistema, incluindo o nome do criador (para administradores).
        """
        reports = Report.query.all()
        return [{
            "id": report.id,
            "filename": report.filename,
            "user_id": report.user_id,
            "username": User.query.filter_by(id=report.user_id).first().username
        } for report in reports]
