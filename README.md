# 📊 Dashboard Analítico Olist - Eficiência Operacional

**Pipeline ETL + SQL + Machine Learning + Dashboard Interativo**

![Dashboard Preview](https://via.placeholder.com/800x400/1e3a8a/ffffff?text=Dashboard+Olist+Eficiencia+Operacional)

## 🎯 Sobre o Projeto

Análise completa de **118.434 pedidos reais** da Olist (2016–2018).  
Desenvolvido como portfólio forte para posições de **Data Analyst, BI Analyst e Data Engineer**.

**Link do Dashboard ao vivo:**  
👉 **[https://olist-dashboard-sgrjqqmyhxpl8w5u4piwkf.streamlit.app/](https://olist-dashboard-sgrjqqmyhxpl8w5u4piwkf.streamlit.app/)**

## 🛠️ Tecnologias Utilizadas

- **Python** + Pandas
- **SQLite** + SQL
- **Scikit-learn** — Random Forest ( **93.7% acurácia** )
- **Streamlit** + Plotly (visualizações interativas)

## ✨ Principais Funcionalidades

- **ETL completo** — ingestão, limpeza e consolidação dos dados
- KPIs operacionais: Taxa de atraso, Ticket médio, Volume por região
- Análise por Estado, Categoria de Produto e Período
- **Previsão de atraso de entrega** em tempo real
- Filtros interativos (Estados, Período, Faixa de Preço)

## 📈 Como Executar Localmente

```bash
# 1. ETL
python etl/etl_pipeline.py

# 2. Treinar modelo de previsão
python models/train_model.py

# 3. Rodar dashboard
python -m streamlit run streamlit/app.py