import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import spacy
from fpdf import FPDF
import matplotlib.pyplot as plt
import os
import threading

# Entidade Dataset
class Dataset:
    def __init__(self, caminho_arquivo):
        self.caminho_arquivo = caminho_arquivo
        self.dados = None

    def carregar_dados(self):
        try:
            self.dados = pd.read_csv(self.caminho_arquivo)
        except Exception as e:
            raise Exception(f"Erro ao carregar os dados: {e}")

# Entidade Relatorio
class Relatorio:
    def __init__(self, dataset):
        self.dataset = dataset  # Instância de Dataset
        self.descricao = ""
        self.graficos = []  # Caminhos dos gráficos gerados
        self.insights = ""

    def gerar_relatorio(self, analisador_dados, insights_negocio):
        """Gera o relatório completo, incluindo gráficos e insights."""
        # Ajuste aqui para capturar a descrição e os gráficos corretamente
        self.descricao, self.graficos = analisador_dados.gerar_relatorio_descritivo(self.dataset.dados)
        self.insights = insights_negocio.gerar_insights_negocio(self.dataset.dados)

# Entidade Usuario
class Usuario:
    def __init__(self, nome):
        self.nome = nome
        self.relatorios = []

    def gerar_relatorio(self, dataset):
        analisador = AnalisadorDados()
        insights = InsightsNegocio()
        relatorio = Relatorio(dataset)
        relatorio.gerar_relatorio(analisador, insights)
        self.relatorios.append(relatorio)
        return relatorio

# Componente AnalisadorDados (Serviço)
class AnalisadorDados:
    def __init__(self):
        pass  # Não precisamos de inicialização para este serviço

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

    def gerar_grafico_coluna(self, nome_coluna, dados):
        """Gera gráficos dependendo do tipo de coluna"""
        try:
            fig, ax = plt.subplots()
            if pd.api.types.is_numeric_dtype(dados[nome_coluna]):
                dados[nome_coluna].hist(ax=ax, bins=15, edgecolor='black')
                ax.set_title(f"Histograma de {nome_coluna}")
                ax.set_xlabel(nome_coluna)
                ax.set_ylabel("Frequência")
            elif pd.api.types.is_object_dtype(dados[nome_coluna]):
                dados[nome_coluna].value_counts().plot(kind='bar', ax=ax)
                ax.set_title(f"Distribuição de {nome_coluna}")
                ax.set_xlabel(nome_coluna)
                ax.set_ylabel("Frequência")
            elif pd.api.types.is_datetime64_any_dtype(dados[nome_coluna]):
                dados[nome_coluna].value_counts().sort_index().plot(ax=ax)
                ax.set_title(f"Série Temporal de {nome_coluna}")
                ax.set_xlabel("Data")
                ax.set_ylabel("Frequência")

            grafico_path = f"{nome_coluna}_grafico.png"
            plt.savefig(grafico_path)
            plt.close()
            return grafico_path  # Retorna o caminho do gráfico gerado
        except Exception as e:
            print(f"Erro ao gerar gráfico para a coluna {nome_coluna}: {e}")

    def gerar_relatorio_descritivo(self, dados):
        relatorio = f"O conjunto de dados contém {len(dados)} linhas e {len(dados.columns)} colunas.\n"
        graficos = []

        for col in dados.columns:
            relatorio += f"\nAnalisando a coluna '{col}':\n"
            contexto = self.detectar_contexto_coluna(col)

            # Gera gráfico da coluna
            grafico_path = self.gerar_grafico_coluna(col, dados)
            if grafico_path:
                graficos.append(grafico_path)

            if pd.api.types.is_numeric_dtype(dados[col]):
                media_val = dados[col].mean()
                mediana_val = dados[col].median()
                desvio_padrao = dados[col].std()
                valor_max = dados[col].max()
                valor_min = dados[col].min()
                valores_faltantes = dados[col].isnull().sum()

                relatorio += (f"- A média é {media_val:.2f}, a mediana é {mediana_val}, "
                              f"e o desvio padrão é {desvio_padrao:.2f}.\n")
                relatorio += f"- O valor mínimo é {valor_min} e o valor máximo é {valor_max}.\n"

                outliers = dados[(dados[col] < media_val - 3 * desvio_padrao) | (dados[col] > media_val + 3 * desvio_padrao)]
                if not outliers.empty:
                    relatorio += f"- {len(outliers)} valores discrepantes (outliers) detectados.\n"

                if valores_faltantes > 0:
                    relatorio += f"- {valores_faltantes} valores faltantes detectados.\n"

            elif pd.api.types.is_object_dtype(dados[col]):
                contagem_unicos = dados[col].nunique()
                valores_top = dados[col].value_counts().nlargest(3)

                relatorio += f"- Coluna categórica com {contagem_unicos} valores únicos.\n"
                relatorio += f"- Valores mais comuns: {', '.join(map(str, valores_top.index))}.\n"

            elif pd.api.types.is_datetime64_any_dtype(dados[col]):
                data_min = dados[col].min()
                data_max = dados[col].max()
                relatorio += f"- Intervalo de datas de {data_min} a {data_max}.\n"

        return relatorio, graficos

# Serviço para gerar insights de negócios
class InsightsNegocio:
    @staticmethod
    def gerar_insights_negocio(dados):
        insights = "\n--- Insights de Negócios ---\n"
        insights += "Com base na análise, aqui estão alguns possíveis insights de negócios:\n\n"

        if 'preço' in dados.columns or 'custo' in dados.columns:
            coluna_preco = 'preço' if 'preço' in dados.columns else 'custo'
            media_preco = dados[coluna_preco].mean()
            insights += f"- O {coluna_preco} médio é {media_preco:.2f}. Considere ajustar as estratégias de preços.\n"

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

# Serviço para formatação de texto
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

# Serviço para gerar PDF
class GeradorRelatorioPDF:
    def __init__(self, nome_arquivo):
        self.nome_arquivo = nome_arquivo

    def salvar_relatorio_em_pdf(self, relatorio, graficos):
        try:
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            for linha in relatorio.split("\n"):
                pdf.multi_cell(0, 10, linha)

            # Adiciona os gráficos ao PDF
            for grafico_path in graficos:
                pdf.add_page()
                pdf.image(grafico_path, x=10, y=20, w=180)  # Ajusta a posição e o tamanho do gráfico

            pdf.output(self.nome_arquivo)

            # Remove os gráficos temporários
            for grafico_path in graficos:
                os.remove(grafico_path)

        except Exception as e:
            raise Exception(f"Erro ao gerar o PDF: {e}")

# Interface Gráfica atualizada
class InterfaceGrafica:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerador de Relatórios")
        self.root.geometry("600x400")

        # Definir o tema
        style = ttk.Style()
        style.theme_use('clam')

        # Frame principal
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Label e Entry para selecionar o arquivo
        self.label = ttk.Label(main_frame, text="Selecione um arquivo CSV para gerar o relatório:")
        self.label.pack(pady=5)

        self.file_path = tk.StringVar()
        file_frame = ttk.Frame(main_frame)
        file_frame.pack(fill=tk.X, pady=5)

        self.entry = ttk.Entry(file_frame, textvariable=self.file_path, width=50)
        self.entry.pack(side=tk.LEFT, expand=True, fill=tk.X)

        self.btn_selecionar = ttk.Button(file_frame, text="Selecionar Arquivo", command=self.selecionar_arquivo)
        self.btn_selecionar.pack(side=tk.LEFT, padx=5)

        # Label e Entry para selecionar o local de saída
        self.output_label = ttk.Label(main_frame, text="Selecione o local para salvar o relatório PDF:")
        self.output_label.pack(pady=5)

        self.output_path = tk.StringVar()
        output_frame = ttk.Frame(main_frame)
        output_frame.pack(fill=tk.X, pady=5)

        self.output_entry = ttk.Entry(output_frame, textvariable=self.output_path, width=50)
        self.output_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)

        self.btn_selecionar_saida = ttk.Button(output_frame, text="Selecionar Local", command=self.selecionar_local_saida)
        self.btn_selecionar_saida.pack(side=tk.LEFT, padx=5)

        # Botão para gerar o relatório
        self.btn_gerar = ttk.Button(main_frame, text="Gerar Relatório", command=self.gerar_relatorio, state=tk.DISABLED)
        self.btn_gerar.pack(pady=20)

        # Barra de progresso
        self.progress = ttk.Progressbar(main_frame, orient=tk.HORIZONTAL, length=400, mode='indeterminate')
        self.progress.pack(pady=10)

        self.arquivo_selecionado = None
        self.arquivo_saida = None

    def selecionar_arquivo(self):
        self.arquivo_selecionado = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if self.arquivo_selecionado:
            self.file_path.set(self.arquivo_selecionado)
            if self.output_path.get():
                self.btn_gerar.config(state=tk.NORMAL)

    def selecionar_local_saida(self):
        self.arquivo_saida = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if self.arquivo_saida:
            self.output_path.set(self.arquivo_saida)
            if self.file_path.get():
                self.btn_gerar.config(state=tk.NORMAL)

    def gerar_relatorio(self):
        if self.arquivo_selecionado and self.arquivo_saida:
            self.progress.start()
            self.btn_gerar.config(state=tk.DISABLED)
            thread = threading.Thread(target=self.run_relatorio)
            thread.start()
        else:
            messagebox.showwarning("Aviso", "Por favor, selecione um arquivo de entrada e um local de saída.")

    def run_relatorio(self):
        try:
            usuario = Usuario("Admin")  # Apenas como exemplo de entidade
            dataset = Dataset(self.arquivo_selecionado)
            dataset.carregar_dados()
            relatorio = usuario.gerar_relatorio(dataset)
            formatador = FormatadorLinguagemNatural()

            # Concatena a descrição e os insights
            relatorio_formatado = formatador.formatar_relatorio(relatorio.descricao + relatorio.insights)

            gerador_pdf = GeradorRelatorioPDF(self.arquivo_saida)
            gerador_pdf.salvar_relatorio_em_pdf(relatorio_formatado, relatorio.graficos)

            # Exibe mensagem de sucesso na thread principal
            self.root.after(0, lambda: messagebox.showinfo("Resultado", "Relatório gerado com sucesso!"))
        except Exception as e:
            # Exibe mensagem de erro na thread principal
            self.root.after(0, lambda: messagebox.showerror("Erro", f"Ocorreu um erro: {e}"))
        finally:
            # Para a barra de progresso e reativa o botão na thread principal
            self.root.after(0, self.progress.stop)
            self.root.after(0, lambda: self.btn_gerar.config(state=tk.NORMAL))

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfaceGrafica(root)
    root.mainloop()
