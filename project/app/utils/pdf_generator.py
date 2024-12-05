from fpdf import FPDF

class PDFGenerator:
    @staticmethod
    def generate_pdf(report_content, charts, filepath):
        try:
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, report_content)

            for chart in charts:
                pdf.add_page()
                pdf.image(chart, x=10, y=20, w=180)

            pdf.output(filepath)
        except Exception as e:
            raise ValueError(f"Erro ao criar PDF: {e}")
