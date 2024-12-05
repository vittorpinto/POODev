from app.models.database import db, Report, User 

class ReportService:
    @staticmethod
    def save_file(file, filename):
        UPLOAD_FOLDER = 'uploads'
        filepath = f"{UPLOAD_FOLDER}/{filename}"
        file.save(filepath)
        return filepath

    @staticmethod
    def enqueue_report(filepath, user_id):
        from app import fila 
        job = fila.enqueue('app.tasks.generate_report.generate_report', filepath, user_id)
        return job.id

    @staticmethod
    def check_job_status(job_id):
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
        reports = Report.query.filter_by(user_id=user_id).all()
        return [{
            "id": report.id,
            "filename": report.filename,
            "user_id": report.user_id
        } for report in reports]

    @staticmethod
    def get_reports_for_user_with_users(user_id):
        reports = Report.query.filter_by(user_id=user_id).all()
        return [{
            "id": report.id,
            "filename": report.filename,
            "user_id": report.user_id,
            "username": User.query.filter_by(id=report.user_id).first().username
        } for report in reports]

    @staticmethod
    def get_all_reports_with_users():
        reports = Report.query.all()
        return [{
            "id": report.id,
            "filename": report.filename,
            "user_id": report.user_id,
            "username": User.query.filter_by(id=report.user_id).first().username
        } for report in reports]
