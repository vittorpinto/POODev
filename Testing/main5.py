import pandas as pd
import spacy
from fpdf import FPDF

# Carregar o modelo de linguagem do spaCy com o sentencizer
nlp = spacy.blank("en")
sentencizer = nlp.add_pipe('sentencizer')  # Adicionando o sentencizer para identificar sentenças

# Função para carregar e analisar os dados
def load_and_profile_data(file_path):
    try:
        data = pd.read_csv(file_path)
        print("Data loaded successfully.")
        profile = data.describe(include='all')  # Gera o perfil estatístico para todas as colunas
        print("Data profile generated.")
        return data, profile
    except Exception as e:
        print(f"Error loading data: {e}")
        return None, None

# Função para gerar o relatório detalhado
def generate_insightful_report_v2(data):
    insights_report = ""

    # Introdução do conjunto de dados
    insights_report += f"The dataset contains {len(data)} rows and {len(data.columns)} columns.\n"

    for col in data.columns:
        insights_report += f"\nAnalyzing the column '{col}':\n"
        if pd.api.types.is_numeric_dtype(data[col]):
            # Análise numérica
            mean_val = data[col].mean()
            median_val = data[col].median()
            std_dev = data[col].std()
            max_val = data[col].max()
            min_val = data[col].min()
            missing_count = data[col].isnull().sum()

            insights_report += f"- The mean is {mean_val:.2f}, median is {median_val}, and standard deviation is {std_dev:.2f}.\n"
            insights_report += f"- Min value is {min_val} and max is {max_val}.\n"

            outliers = data[(data[col] < mean_val - 3 * std_dev) | (data[col] > mean_val + 3 * std_dev)]
            if not outliers.empty:
                insights_report += f"- {len(outliers)} outliers detected.\n"

            if missing_count > 0:
                insights_report += f"- {missing_count} missing values detected.\n"

        elif pd.api.types.is_object_dtype(data[col]):
            # Análise de colunas categóricas
            unique_count = data[col].nunique()
            top_values = data[col].value_counts().nlargest(3)

            insights_report += f"- Categorical column with {unique_count} unique values.\n"
            insights_report += f"- Most common values: {', '.join(map(str, top_values.index))}.\n"
            if unique_count > 50:
                insights_report += "- High number of unique categories.\n"

        elif pd.api.types.is_datetime64_any_dtype(data[col]):
            min_date = data[col].min()
            max_date = data[col].max()
            insights_report += f"- Date range from {min_date} to {max_date}.\n"

    return insights_report

# Função para gerar insights de negócios com base nos dados
def generate_business_insights(data):
    insights = "\n--- Business Insights ---\n"
    insights += "Based on the analysis, here are some potential business insights:\n\n"

    if 'price' in data.columns:
        # Exemplo de insight relacionado a preço
        avg_price = data['price'].mean()
        insights += f"- The average price is {avg_price:.2f}. Consider adjusting pricing strategies based on regional or seasonal demand.\n"

    if 'sales' in data.columns:
        # Exemplo de insight relacionado a vendas
        total_sales = data['sales'].sum()
        insights += f"- Total sales amount to {total_sales}. Focus on the top-performing products or services to increase revenue.\n"

    if 'customer_age' in data.columns:
        # Exemplo de insight relacionado a clientes
        avg_age = data['customer_age'].mean()
        insights += f"- The average customer age is {avg_age:.2f}. Consider marketing strategies tailored to this age group.\n"

    # Verificando se há colunas de datas para insights temporais
    date_columns = [col for col in data.columns if pd.api.types.is_datetime64_any_dtype(data[col])]
    if date_columns:
        insights += "- Temporal analysis suggests optimizing operations around key dates or seasons for better performance.\n"

    # Análise genérica sobre variabilidade dos dados
    highly_variable_columns = []
    for col in data.columns:
        if pd.api.types.is_numeric_dtype(data[col]):
            std_dev = data[col].std()
            if std_dev > data[col].mean() * 0.5:  # Exemplo de critério de alta variabilidade
                highly_variable_columns.append(col)

    if highly_variable_columns:
        insights += f"- The following columns show high variability, which may indicate inconsistent performance or significant differences across instances:\n  {', '.join(highly_variable_columns)}.\n"

    return insights

# Função para formatar o texto com spaCy
def generate_natural_language_report(narrative_report):
    try:
        # Usa o spaCy para dividir o texto em sentenças e reformatar
        doc = nlp(narrative_report)
        formatted_report = []
        for sentence in doc.sents:
            formatted_report.append(str(sentence).strip())

        # Junta o texto com uma estrutura coesa
        final_report = "\n".join(formatted_report)  # Cada sentença em nova linha
        
        return final_report
    except Exception as e:
        print(f"Error generating text with spaCy: {e}")
        return narrative_report

# Função para salvar o relatório no PDF
def save_report_as_pdf(report_content, file_name):
    try:
        # Criação do objeto PDF
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        pdf.set_font("Arial", size=12)

        # Quebrar o conteúdo do relatório em linhas
        for line in report_content.split("\n"):
            pdf.multi_cell(0, 10, line)

        # Salvar o PDF
        pdf.output(file_name)
        print(f"Report saved as {file_name}.")
    except Exception as e:
        print(f"Error generating PDF: {e}")

# Função principal para gerar o relatório final
def main(file_path):
    data, _ = load_and_profile_data(file_path)
    
    if data is not None:
        # Gera um relatório analítico com sugestões e padrões detectados
        insightful_report = generate_insightful_report_v2(data)
        
        # Usa o spaCy para formatar o relatório de forma mais natural
        natural_language_report = generate_natural_language_report(insightful_report)
        
        # Gera insights de negócios a partir dos dados
        business_insights = generate_business_insights(data)
        
        # Adiciona os insights ao final do relatório
        full_report = natural_language_report + business_insights
        
        # Salva o relatório gerado em um arquivo PDF
        save_report_as_pdf(full_report, "generated_natural_language_report.pdf")
        
    else:
        print("Unable to generate the report due to an error in the data.")

# Execução exemplo (substitua com o caminho correto para seu arquivo)
file_path = "data.csv"  # Atualize com seu caminho correto
main(file_path)
