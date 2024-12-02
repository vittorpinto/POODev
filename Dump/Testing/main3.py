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

# Função para gerar um resumo narrativo das colunas numéricas e categóricas
def generate_narrative_report(data):
    narrative_report = ""

    # Introdução ao conjunto de dados
    narrative_report += f"O conjunto de dados analisado contém {len(data)} linhas e {len(data.columns)} colunas.\n"
    narrative_report += "Ele contém informações detalhadas sobre músicas e suas características.\n"
    
    # Iterar sobre as colunas
    for col in data.columns:
        narrative_report += f"\nAgora, vamos falar sobre a coluna '{col}':\n"
        
        if pd.api.types.is_numeric_dtype(data[col]):
            # Descrição narrativa para colunas numéricas
            narrative_report += f"Esta coluna é numérica e apresenta uma média de {data[col].mean():.2f}. "
            narrative_report += f"O valor mínimo encontrado foi {data[col].min()} e o valor máximo foi {data[col].max()}. "
            narrative_report += f"A mediana é {data[col].median()} e o desvio padrão é {data[col].std():.2f}. "
        elif pd.api.types.is_object_dtype(data[col]):
            # Descrição narrativa para colunas categóricas
            top_values = data[col].value_counts().nlargest(3)
            narrative_report += f"Esta é uma coluna categórica e os valores mais comuns são: {', '.join(map(str, top_values.index))}. "
            narrative_report += f"A coluna contém um total de {data[col].nunique()} valores únicos."
        elif pd.api.types.is_datetime64_any_dtype(data[col]):
            # Descrição para colunas de data
            narrative_report += f"Esta coluna contém informações de data. A data mais antiga é {data[col].min()} e a mais recente é {data[col].max()}."
        
        # Verificar valores ausentes
        missing_count = data[col].isnull().sum()
        if missing_count > 0:
            narrative_report += f" Esta coluna tem {missing_count} valores ausentes."
        else:
            narrative_report += " Não há valores ausentes nesta coluna."
        
        narrative_report += "\n"

    return narrative_report

# Função para dividir o texto em partes menores, controlando o tamanho
def split_text_into_chunks(text, max_token_length=1024):
    words = text.split()
    chunks = []
    
    current_chunk = []
    current_length = 0
    
    for word in words:
        current_length += len(word) + 1  # +1 to account for the space
        if current_length <= max_token_length:
            current_chunk.append(word)
        else:
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]  # Start a new chunk
            current_length = len(word) + 1
    
    # Add the last chunk if it exists
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks

# Função para transformar a descrição técnica em uma explicação contínua e natural
def generate_natural_language_report(narrative_report):
    try:
        # Inicializar o pipeline de geração de texto com GPT-2 (ou distilgpt2 para ser mais leve)
        text_generator = pipeline("text-generation", model="distilgpt2")
        
        generated_report = ""
        # Dividir o relatório em pedaços menores de até 1024 tokens
        chunks = split_text_into_chunks(narrative_report)
        
        for chunk in chunks:
            # Gerar texto para cada pedaço com truncation=True para evitar erro de tamanho
            generated_chunk = text_generator(chunk, max_new_tokens=200, truncation=True)[0]['generated_text']
            generated_report += generated_chunk + "\n"
        
        return generated_report
    except Exception as e:
        print(f"Erro ao gerar texto com Transformers: {e}")
        return narrative_report

# Função principal para gerar o relatório final
def main(file_path):
    data, _ = load_and_profile_data(file_path)
    
    if data is not None:
        # Gerar um relatório narrativo inicial
        narrative_report = generate_narrative_report(data)
        
        # Usar o transformers para transformar o relatório em texto contínuo e mais natural
        natural_language_report = generate_natural_language_report(narrative_report)
        
        # Salvar o relatório gerado em um arquivo
        with open("generated_natural_language_report.txt", "w", encoding="utf-8") as f:
            f.write(natural_language_report)
        
        print("Relatório gerado e salvo com sucesso.")
    else:
        print("Não foi possível gerar o relatório devido a um erro nos dados.")

# Exemplo de execução (trocar o caminho do arquivo)
file_path = "data.csv"  # Atualize com o caminho correto do seu arquivo
main(file_path)