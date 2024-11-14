# models.py
import os
import pandas as pd
import spacy
import matplotlib.pyplot as plt
from fpdf import FPDF

plt.switch_backend('Agg')  

class Dataset:
    def __init__(self, caminho_arquivo):
        self.caminho_arquivo = caminho_arquivo
        self.dados = None

    def carregar_dados(self):
        try:
            self.dados = pd.read_csv(self.caminho_arquivo)
        except Exception as e:
            raise Exception(f"Erro ao carregar os dados: {e}")

class Relatorio:
    def __init__(self, dataset):
        self.dataset = dataset
        self.descricao = ""
        self.graficos = []
        self.insights = ""

    def gerar_relatorio(self, analisador_dados, insights_negocio):
        self.descricao, self.graficos = analisador_dados.gerar_relatorio_descritivo(self.dataset.dados)
        self.insights = insights_negocio.gerar_insights_negocio(self.dataset.dados)

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

class AnalisadorDados:
    def __init__(self):
        pass

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
            return grafico_path
        except Exception as e:
            print(f"Erro ao gerar gráfico para a coluna {nome_coluna}: {e}")

    def gerar_relatorio_descritivo(self, dados):
        relatorio = f"O conjunto de dados contém {len(dados)} linhas e {len(dados.columns)} colunas.\n"
        graficos = []

        for col in dados.columns:
            relatorio += f"\nAnalisando a coluna '{col}':\n"
            contexto = self.detectar_contexto_coluna(col)
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

class FormatadorLinguagemNatural:
    def __init__(self):
        self.nlp = spacy.load("pt_core_news_sm")
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

    def salvar_relatorio_em_pdf(self, relatorio, graficos):
        try:
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            for linha in relatorio.split("\n"):
                pdf.multi_cell(0, 10, linha)

            for grafico_path in graficos:
                pdf.add_page()
                pdf.image(grafico_path, x=10, y=20, w=180)

            pdf.output(self.nome_arquivo)

            for grafico_path in graficos:
                os.remove(grafico_path)

        except Exception as e:
            raise Exception(f"Erro ao gerar o PDF: {e}")
