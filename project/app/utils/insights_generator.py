class InsightsGenerator:
    @staticmethod
    def generate_insights(data):
        insights = "--- Insights de Negócios ---\\n"
        if "preço" in data.columns:
            avg_price = data["preço"].mean()
            insights += f"- O preço médio dos produtos é {avg_price:.2f}.\\n"
        if "vendas" in data.columns:
            total_sales = data["vendas"].sum()
            insights += f"- Total de vendas registrado: {total_sales}.\\n"
        return insights