import os
from flask import Flask  # Certifique-se de importar Flask
from database import db, User, Report
from models import Dataset, Usuario, FormatadorLinguagemNatural, GeradorRelatorioPDF

def gerar_relatorio_pdf(filepath, usuario_nome, user_id, database_uri):
    try:
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(app)

        with app.app_context():
            # Obter o usuário logado pelo user_id
            user = User.query.get(user_id)
            if not user:
                raise Exception("Usuário logado não encontrado")

            # Obter o administrador
            admin_user = User.query.filter_by(username="Admin").first()
            if not admin_user:
                raise Exception("Administrador não encontrado")

            # Carregar o dataset e gerar o relatório
            dataset = Dataset(filepath)
            dataset.carregar_dados()

            usuario = Usuario(usuario_nome)
            relatorio = usuario.gerar_relatorio(dataset)

            # Formatar e salvar o relatório em PDF
            formatador = FormatadorLinguagemNatural()
            relatorio_formatado = formatador.formatar_relatorio(
                relatorio.descricao + relatorio.insights
            )

            pdf_filename = os.path.join("uploads/", f"relatorio_{usuario_nome}.pdf")
            gerador_pdf = GeradorRelatorioPDF(pdf_filename)
            gerador_pdf.salvar_relatorio_em_pdf(
                relatorio_formatado, relatorio.graficos
            )

            # Salvar o relatório associado ao usuário logado
            user_report = Report(filename=pdf_filename, user_id=user.id)
            db.session.add(user_report)

            # Salvar o relatório associado ao administrador
            admin_report = Report(filename=pdf_filename, user_id=admin_user.id)
            db.session.add(admin_report)

            db.session.commit()

            return pdf_filename
    except Exception as e:
        raise Exception(f"Erro na geração do relatório: {e}")