import pandas as pd
from transformers import pipeline

# Função para carregar e revisar dados
def load_and_profile_data(file_path):
    try:
        data = pd.read_csv(file_path)
        print("Dados carregados com sucesso.")
        profile = data.describe(include='all')  # Gerar perfil estatístico para todas as colunas
        print("Perfil dos dados gerado.")
        return data, profile
    except Exception as e:
        print(f"Erro ao carregar os dados: {e}")
        return None, None

# Função para gerar um relatório genérico baseado em qualquer conjunto de dados
def generate_generic_report(data, profile):
    # Iniciando o relatório com um resumo
    report_content = "### Relatório sobre o conjunto de dados ###\n\n"
    report_content += f"O conjunto de dados contém {len(data)} linhas e {len(data.columns)} colunas.\n\n"
    
    # Listando todas as colunas
    report_content += "As colunas presentes no dataset são:\n"
    for col in data.columns:
        report_content += f"- {col}\n"
    
    report_content += "\n### Estatísticas Gerais ###\n\n"
    
    # Para cada coluna, vamos gerar insights com base no tipo de dado
    for col in data.columns:
        report_content += f"\n**Coluna: {col}**\n"
        report_content += f"Tipo de dado: {data[col].dtype}\n"
        
        if pd.api.types.is_numeric_dtype(data[col]):
            # Se for numérico, forneça estatísticas como média, mediana, mínimo, máximo, etc.
            report_content += f"- Média: {data[col].mean()}\n"
            report_content += f"- Mediana: {data[col].median()}\n"
            report_content += f"- Valor mínimo: {data[col].min()}\n"
            report_content += f"- Valor máximo: {data[col].max()}\n"
            report_content += f"- Desvio padrão: {data[col].std()}\n"
        elif pd.api.types.is_object_dtype(data[col]):
            # Se for categórico ou string, forneça insights como os valores mais comuns
            top_values = data[col].value_counts().nlargest(3)
            report_content += f"- Valores mais comuns: {top_values.to_dict()}\n"
            report_content += f"- Total de valores únicos: {data[col].nunique()}\n"
        elif pd.api.types.is_datetime64_any_dtype(data[col]):
            # Se for uma coluna de data, fornecer insights sobre o período
            report_content += f"- Primeira data: {data[col].min()}\n"
            report_content += f"- Última data: {data[col].max()}\n"
        
        # Adicionar a quantidade de valores ausentes
        missing_count = data[col].isnull().sum()
        if missing_count > 0:
            report_content += f"- Total de valores ausentes: {missing_count} ({(missing_count/len(data))*100:.2f}%)\n"
        else:
            report_content += "- Não há valores ausentes.\n"
    
    # Finalizando com as estatísticas gerais do dataset
    report_content += "\n### Estatísticas Resumidas do Conjunto de Dados ###\n"
    report_content += profile.to_string()  # Adicionar as estatísticas gerais do perfil gerado pelo pandas.describe()
    
    return report_content

# Função para gerar um texto explicativo usando o modelo transformers
def generate_natural_language_report(report_content):
    try:
        # Inicializar o pipeline de geração de texto com GPT-2 (ou distilgpt2 para ser mais leve)
        text_generator = pipeline("text-generation", model="distilgpt2")
        
        # Usar o modelo para gerar uma versão em linguagem natural do relatório
        generated_report = text_generator(report_content, max_length=300)[0]['generated_text']
        return generated_report
    except Exception as e:
        print(f"Erro ao gerar texto com Transformers: {e}")
        return report_content

# Função principal para gerar o relatório final
def main(file_path):
    data, profile = load_and_profile_data(file_path)
    
    if data is not None:
        # Gera o relatório técnico
        technical_report = generate_generic_report(data, profile)
        
        # Usar o transformers para gerar uma versão mais amigável em linguagem natural
        natural_language_report = generate_natural_language_report(technical_report)
        
        # Salvar o relatório gerado em um arquivo
        with open("generated_natural_language_report.txt", "w") as f:
            f.write(natural_language_report)
        
        print("Relatório gerado e salvo com sucesso.")
    else:
        print("Não foi possível gerar o relatório devido a um erro nos dados.")

# Exemplo de execução (trocar o caminho do arquivo)
file_path = "data.csv"  # Atualize com o caminho correto do seu arquivo
main(file_path)
