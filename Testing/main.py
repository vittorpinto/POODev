#%%
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

#%%
class File:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None
    
    def load_file(self):
        # Identifica o tipo de arquivo e carrega os dados
        if self.file_path.endswith('.csv'):
            self.data = self._load_csv()
        elif self.file_path.endswith('.json'):
            self.data = self._load_json()
    
    def _load_csv(self):
        # Carregar e processar o CSV, transformando em dados
        import csv
        data = []
        with open(self.file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data.append(row)
        return data
    
    def _load_json(self):
        # Carregar e processar o JSON
        import json
        with open(self.file_path) as json_file:
            return json.load(json_file)

    def get_data(self):
        return self.data

class Report:
    def __init__(self, data):
        self.data = data
    
    def generate_summary(self):
        # Aqui você pode processar os dados para gerar resumos ou estatísticas
        summary = {
            'total_entries': len(self.data),
            # Adicione mais resumos conforme necessário
        }
        return summary



class ReportGenerator:
    def __init__(self, report):
        self.report = report
    
    def generate_pdf(self, output_path):
        # Utilizando ReportLab para gerar PDF
        c = canvas.Canvas(output_path, pagesize=letter)
        c.drawString(100, 750, "Relatório Gerado")
        
        # Adicionar dados do relatório no PDF
        summary = self.report.generate_summary()
        c.drawString(100, 730, f"Total de Registros: {summary['total_entries']}")
        
        # Exemplo de impressão de uma lista de dados
        y = 700
        for idx, entry in enumerate(self.report.data):
            c.drawString(100, y, f"Entrada {idx + 1}: {entry}")
            y -= 20
        
        c.save()


class UI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Gerador de Relatórios")
    
    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("JSON files", "*.json")])
        if file_path:
            file = File(file_path)
            file.load_file()
            report = Report(file.get_data())
            report_generator = ReportGenerator(report)
            
            output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
            if output_path:
                report_generator.generate_pdf(output_path)
                messagebox.showinfo("Sucesso", "Relatório gerado com sucesso!")
    
    def run(self):
        btn = tk.Button(self.root, text="Selecionar Arquivo", command=self.select_file)
        btn.pack(pady=20)
        self.root.mainloop()

# Para rodar a interface gráfica
if __name__ == "__main__":
    ui = UI()
    ui.run()
