import pandas as pd
import matplotlib.pyplot as plt
import os

plt.switch_backend('Agg')  # Usar backend sem interface gráfica

class DataAnalyzer:
    CHARTS_FOLDER = os.path.join(os.getcwd(), "charts")  

    def __init__(self, filepath):
        self.filepath = filepath
        self.data = None

    def load_data(self):
        try:
            self.data = pd.read_csv(self.filepath)
        except Exception as e:
            raise ValueError(f"Erro ao carregar os dados: {e}")

    def save_chart(self, column_name):

        if not os.path.exists(DataAnalyzer.CHARTS_FOLDER):
            os.makedirs(DataAnalyzer.CHARTS_FOLDER)

        chart_path = os.path.join(DataAnalyzer.CHARTS_FOLDER, f"{column_name}_chart.png")
        try:
            plt.savefig(chart_path)
            plt.close()  
            return chart_path
        except Exception as e:
            print(f"Erro ao salvar gráfico para {column_name}: {e}")
            return None

    def detect_column_context(self, column_name):

        if "preço" in column_name.lower() or "custo" in column_name.lower():
            return "financeiro"
        elif "cliente" in column_name.lower() or "idade" in column_name.lower():
            return "demográfico"
        elif "data" in column_name.lower() or "ano" in column_name.lower():
            return "temporal"
        return "outro"

    def generate_column_chart(self, column_name):
        try:
            plt.figure()  
            if pd.api.types.is_numeric_dtype(self.data[column_name]):
                self.data[column_name].plot.hist(bins=15, edgecolor='black')
                plt.title(f"Histograma de {column_name}")
                plt.xlabel(column_name)
                plt.ylabel("Frequência")
            elif pd.api.types.is_object_dtype(self.data[column_name]):
                self.data[column_name].value_counts().plot(kind='bar')
                plt.title(f"Distribuição de {column_name}")
                plt.xlabel(column_name)
                plt.ylabel("Frequência")

            chart_path = os.path.join(DataAnalyzer.CHARTS_FOLDER, f"{column_name}_chart.png")
            return self.save_chart(column_name)
        except Exception as e:
            print(f"Erro ao gerar gráfico para {column_name}: {e}")
            return None

    def generate_descriptive_report(self):

        if self.data is None:
            raise ValueError("Os dados não foram carregados. Use 'load_data()' antes de gerar relatórios.")

        report = f"O conjunto de dados contém {len(self.data)} linhas e {len(self.data.columns)} colunas.\n"
        charts = []

        for column in self.data.columns:
            report += f"\nAnálise da coluna '{column}':\n"
            context = self.detect_column_context(column)
            report += f"- Contexto detectado: {context}\n"

            if pd.api.types.is_numeric_dtype(self.data[column]):
                report += f"- Média: {self.data[column].mean():.2f}\n"
                report += f"- Máximo: {self.data[column].max()}\n"
                report += f"- Mínimo: {self.data[column].min()}\n"
            elif pd.api.types.is_object_dtype(self.data[column]):
                report += f"- Valores únicos: {self.data[column].nunique()}\n"

            chart_path = self.generate_column_chart(column)
            if chart_path:
                charts.append(chart_path)

        return report, charts
