import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import spacy
from fpdf import FPDF

class AnalisadorDados:
    def __init__(self, caminho_arquivo):
        self.caminho_arquivo = caminho_arquivo
        self.dados = None
        self.perfil = None

    def carregar_e_analisar_dados(self):
        try:
            self.dados = pd.read_csv(self.caminho_arquivo)
            self.perfil = self.dados.describe(include='all')
        except Exception as e:
            raise Exception(f"Erro ao carregar os dados: {e}")

    def detectar_contexto_coluna(self, nome_coluna):
        if "preço" in nome_coluna.lower() or "custo" in nome_coluna.lower() or "receita" in nome_coluna.lower():
            return "financeiro"
        elif "cliente" in nome_coluna.lower() or "idade" in nome_coluna.lower() or "gênero" in nome_coluna.lower():
            return "cliente"
        elif "data" in nome_coluna.lower() or "tempo" in nome_coluna.lower() or "ano" in nome_coluna.lower():
            return "temporal"
        elif "vendas" in nome_coluna.lower() or "quantidade" in nome_coluna.lower() or "produto" in nome_coluna.lower():
            return "produto"
        else:
            return "outro"

    def gerar_relatorio_descritivo(self):
        if self.dados is None:
            return ""

        relatorio = f"O conjunto de dados contém {len(self.dados)} linhas e {len(self.dados.columns)} colunas.\n"

        for col in self.dados.columns:
            relatorio += f"\nAnalisando a coluna '{col}':\n"
            contexto = self.detectar_contexto_coluna(col)

            if pd.api.types.is_numeric_dtype(self.dados[col]):
                media_val = self.dados[col].mean()
                mediana_val = self.dados[col].median()
                desvio_padrao = self.dados[col].std()
                valor_max = self.dados[col].max()
                valor_min = self.dados[col].min()
                valores_faltantes = self.dados[col].isnull().sum()

                relatorio += (f"- A média é {media_val:.2f}, a mediana é {mediana_val}, "
                              f"e o desvio padrão é {desvio_padrao:.2f}.\n")
                relatorio += f"- O valor mínimo é {valor_min} e o valor máximo é {valor_max}.\n"

                outliers = self.dados[(self.dados[col] < media_val - 3 * desvio_padrao) | (self.dados[col] > media_val + 3 * desvio_padrao)]
                if not outliers.empty:
                    relatorio += f"- {len(outliers)} valores discrepantes (outliers) detectados.\n"

                if valores_faltantes > 0:
                    relatorio += f"- {valores_faltantes} valores faltantes detectados.\n"

                relatorio += self.gerar_insights_contexto_numerico(contexto, media_val, col)

            elif pd.api.types.is_object_dtype(self.dados[col]):
                contagem_unicos = self.dados[col].nunique()
                valores_top = self.dados[col].value_counts().nlargest(3)

                relatorio += f"- Coluna categórica com {contagem_unicos} valores únicos.\n"
                relatorio += f"- Valores mais comuns: {', '.join(map(str, valores_top.index))}.\n"

                relatorio += self.gerar_insights_contexto_categorico(contexto)

            elif pd.api.types.is_datetime64_any_dtype(self.dados[col]):
                data_min = self.dados[col].min()
                data_max = self.dados[col].max()
                relatorio += f"- Intervalo de datas de {data_min} a {data_max}.\n"
                relatorio += "  Esta coluna representa dados temporais. Você pode realizar análises sazonais ou rastrear o desempenho ao longo do tempo.\n"

        return relatorio

    def gerar_insights_contexto_numerico(self, contexto, media_val, nome_coluna):
        insights = ""
        if contexto == "financeiro":
            insights += "  Esta coluna provavelmente representa dados financeiros. Considere analisar tendências de lucratividade ou custos.\n"
            insights += "  A média é relativamente alta, sugerindo transações financeiras grandes.\n" if media_val > 1000 else "  A média parece moderada, o que pode indicar preços típicos de consumo.\n"
        elif contexto == "cliente" and "idade" in nome_coluna.lower():
            insights += "  Esta coluna provavelmente representa dados de clientes. Considere explorar características demográficas.\n"
            insights += "  A média de idade sugere uma base de clientes jovem.\n" if media_val < 30 else "  A média de idade sugere um público mais maduro.\n"
        elif contexto == "produto":
            insights += "  Esta coluna parece estar relacionada ao desempenho de produtos. Você pode analisar a demanda dos produtos.\n"
        return insights

    def gerar_insights_contexto_categorico(self, contexto):
        insights = ""
        if contexto == "cliente":
            insights += "  Esta coluna pode conter informações de clientes. Considere segmentar os clientes com base nesses dados para campanhas de marketing.\n"
        elif contexto == "produto":
            insights += "  Esta coluna provavelmente representa categorias ou identificadores de produtos. Concentre-se nos itens mais populares.\n"
        return insights


class InsightsNegocio:
    @staticmethod
    def gerar_insights_negocio(dados):
        insights = "\n--- Insights de Negócios ---\n"
        insights += "Com base na análise, aqui estão alguns possíveis insights de negócios:\n\n"

        if 'preço' in dados.columns or 'custo' in dados.columns:
            media_preco = dados['preço'].mean() if 'preço' in dados.columns else dados['custo'].mean()
            insights += f"- O preço/custo médio é {media_preco:.2f}. Considere ajustar as estratégias de preços.\n"

        if 'vendas' in dados.columns:
            total_vendas = dados['vendas'].sum()
            insights += f"- O total de vendas é {total_vendas}. Foco nos produtos mais vendidos para otimizar o estoque.\n"

        if 'idade_cliente' in dados.columns:
            media_idade = dados['idade_cliente'].mean()
            insights += f"- A idade média dos clientes é {media_idade:.2f}. As estratégias de marketing podem ser direcionadas a esse público.\n"
            if media_idade < 30:
                insights += "- Os clientes mais jovens tendem a ter hábitos de compra diferentes. Considere oferecer produtos que os atraiam.\n"
            else:
                insights += "- Um público mais velho pode valorizar serviços personalizados ou produtos de alta qualidade.\n"

        return insights


class FormatadorLinguagemNatural:
    def __init__(self):
        self.nlp = spacy.blank("pt")
        self.nlp.add_pipe('sentencizer')

    def formatar_relatorio(self, texto):
        try:
            doc = self.nlp(texto)
            sentencas_formatadas = [str(sentenca).strip() for sentenca in doc.sents]
            return "\n".join(sentencas_formatadas)
        except Exception as e:
            return texto


class GeradorRelatorioPDF:
    def __init__(self, nome_arquivo):
        self.nome_arquivo = nome_arquivo

    def salvar_relatorio_em_pdf(self, conteudo_relatorio):
        try:
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            for linha in conteudo_relatorio.split("\n"):
                pdf.multi_cell(0, 10, linha)

            pdf.output(self.nome_arquivo)
        except Exception as e:
            raise Exception(f"Erro ao gerar o PDF: {e}")


class GeradorRelatorioApp:
    def __init__(self, caminho_arquivo):
        self.caminho_arquivo = caminho_arquivo
        self.analisador_dados = AnalisadorDados(caminho_arquivo)
        self.formatador_linguagem = FormatadorLinguagemNatural()

    def gerar_relatorio(self):
        try:
            self.analisador_dados.carregar_e_analisar_dados()
            relatorio_descritivo = self.analisador_dados.gerar_relatorio_descritivo()
            relatorio_formatado = self.formatador_linguagem.formatar_relatorio(relatorio_descritivo)
            insights_negocios = InsightsNegocio.gerar_insights_negocio(self.analisador_dados.dados)
            relatorio_final = relatorio_formatado + insights_negocios
            gerador_pdf = GeradorRelatorioPDF("relatorio_gerado.pdf")
            gerador_pdf.salvar_relatorio_em_pdf(relatorio_final)
            return "Relatório gerado com sucesso!"
        except Exception as e:
            return str(e)


# Interface Gráfica
class InterfaceGrafica:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerador de Relatórios")
        self.root.geometry("400x200")

        self.label = tk.Label(root, text="Selecione um arquivo CSV para gerar o relatório:")
        self.label.pack(pady=10)

        self.btn_selecionar = tk.Button(root, text="Selecionar Arquivo", command=self.selecionar_arquivo)
        self.btn_selecionar.pack(pady=10)

        self.btn_gerar = tk.Button(root, text="Gerar Relatório", command=self.gerar_relatorio, state=tk.DISABLED)
        self.btn_gerar.pack(pady=10)

        self.arquivo_selecionado = None

    def selecionar_arquivo(self):
        self.arquivo_selecionado = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if self.arquivo_selecionado:
            self.btn_gerar.config(state=tk.NORMAL)

    def gerar_relatorio(self):
        if self.arquivo_selecionado:
            app = GeradorRelatorioApp(self.arquivo_selecionado)
            resultado = app.gerar_relatorio()
            messagebox.showinfo("Resultado", resultado)


if __name__ == "__main__":
    root = tk.Tk()
    app = InterfaceGrafica(root)
    root.mainloop()
