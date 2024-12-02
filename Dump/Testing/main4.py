import pandas as pd
from transformers import pipeline

# Function to load and profile data
def load_and_profile_data(file_path):
    try:
        data = pd.read_csv(file_path)
        print("Data loaded successfully.")
        profile = data.describe(include='all')  # Generate statistical profile for all columns
        print("Data profile generated.")
        return data, profile
    except Exception as e:
        print(f"Error loading data: {e}")
        return None, None

# A more detailed chunk processing for better result control
def generate_insightful_report_v2(data):
    insights_report = ""

    # Introdução do conjunto de dados
    insights_report += f"The dataset contains {len(data)} rows and {len(data.columns)} columns.\n"
    insights_report += "This dataset provides detailed information about song features.\n"

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

# Function to split text into smaller chunks, controlling the length
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

# Function to transform the technical description into more structured natural language
def generate_natural_language_report(narrative_report):
    try:
        # Initialize the text generation pipeline with GPT-2 (or distilgpt2 for lighter usage)
        text_generator = pipeline("text-generation", model="distilgpt2")
        
        generated_report = ""
        # Split the report into smaller chunks of up to 500 tokens (reduced for more accuracy)
        chunks = split_text_into_chunks(narrative_report, max_token_length=500)
        
        for chunk in chunks:
            # Generate text for each chunk with truncation=True to avoid size errors
            generated_chunk = text_generator(chunk, max_new_tokens=150, truncation=True)[0]['generated_text']
            
            # Post-process: Avoid excessive repetition
            generated_chunk = generated_chunk.replace('The minimum value is', '', 1)
            generated_report += generated_chunk + "\n"
        
        return generated_report
    except Exception as e:
        print(f"Error generating text with Transformers: {e}")
        return narrative_report

# Main function to generate the final report
def main(file_path):
    data, _ = load_and_profile_data(file_path)
    
    if data is not None:
        # Generate an insightful report with suggested actions and patterns
        insightful_report = generate_insightful_report_v2(data)
        
        # Use transformers to convert the report into a more natural continuous text
        natural_language_report = generate_natural_language_report(insightful_report)
        
        # Save the generated report to a file
        with open("generated_natural_language_report.txt", "w", encoding="utf-8") as f:
            f.write(natural_language_report)
        
        print("Report generated and saved successfully.")
    else:
        print("Unable to generate the report due to an error in the data.")

# Example execution (replace with your actual file path)
file_path = "data.csv"  # Update with your correct file path
main(file_path)
