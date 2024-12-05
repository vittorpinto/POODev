import os
from flask import current_app
from app.utils.data_analyzer import DataAnalyzer
from app.utils.insights_generator import InsightsGenerator
from app.utils.pdf_generator import PDFGenerator
from app.models.database import db, Report
from app import create_app  # Import para criar o contexto da aplicação

def generate_report(filepath, user_id):
    """
    Função que realiza a geração de relatório com base nos dados do CSV.
    """
    try:
        print(f"Iniciando geração de relatório para o arquivo: {filepath}, usuário: {user_id}")

        # Garantir o contexto da aplicação
        app = create_app()
        with app.app_context():
            # Carregar os dados
            analyzer = DataAnalyzer(filepath)
            analyzer.load_data()

            # Gerar relatório descritivo
            descriptive_report, charts = analyzer.generate_descriptive_report()

            # Gerar insights
            insights = InsightsGenerator.generate_insights(analyzer.data)

            # Formatar o relatório final
            report_content = f"{descriptive_report}\n\n{insights}"

            # Salvar o relatório em PDF
            report_filename = f"report_{user_id}_{os.path.basename(filepath).split('.')[0]}.pdf"
            report_path = os.path.join("uploads", report_filename)
            PDFGenerator.generate_pdf(report_content, charts, report_path)

            # Registrar no banco de dados
            report = Report(filename=report_filename, user_id=user_id)
            db.session.add(report)
            db.session.commit()

            # Limpar gráficos temporários
            for chart in charts:
                os.remove(chart)

            print(f"Relatório gerado: {report_path}")
            return report_path
    except Exception as e:
        print(f"Erro ao gerar relatório: {e}")
        return None
