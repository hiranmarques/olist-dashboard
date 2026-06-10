# 📊 Dashboard Analítico Olist - Eficiência Operacional

**Pipeline ETL + SQL + Previsão de Atraso** usando dados reais de 118 mil pedidos.

![Dashboard](https://via.placeholder.com/800x400?text=Dashboard+Olist)

## Tecnologias
- **Python** + Pandas
- **SQLite** + SQL
- **Scikit-learn** → Random Forest (93.7% acurácia)
- **Streamlit** + Plotly

## Funcionalidades
- Análise completa de atrasos, ticket médio e volume por estado/categoria
- Filtros interativos (estado, período, preço)
- **Previsão de atraso** em tempo real
- KPIs operacionais relevantes

## Como executar localmente
```bash
# 1. ETL
python etl/etl_pipeline.py

# 2. Treinar modelo
python models/train_model.py

# 3. Rodar dashboard
python -m streamlit run streamlit/app.py