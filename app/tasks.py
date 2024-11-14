# tasks.py
import os
from models import Dataset, Usuario, FormatadorLinguagemNatural, GeradorRelatorioPDF  # Importa as classes de models.py

def gerar_relatorio_pdf(filepath, usuario_nome):
    try:
        dataset = Dataset(filepath)
        dataset.carregar_dados()

        usuario = Usuario(usuario_nome)
        relatorio = usuario.gerar_relatorio(dataset)

        formatador = FormatadorLinguagemNatural()
        relatorio_formatado = formatador.formatar_relatorio(relatorio.descricao + relatorio.insights)

        pdf_filename = os.path.join("uploads/", f"relatorio_{usuario_nome}.pdf")
        gerador_pdf = GeradorRelatorioPDF(pdf_filename)
        gerador_pdf.salvar_relatorio_em_pdf(relatorio_formatado, relatorio.graficos)
        
        return pdf_filename
    except Exception as e:
        raise Exception(f"Erro na geração do relatório: {e}")
