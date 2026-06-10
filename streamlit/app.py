import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
import pickle

st.set_page_config(page_title="Olist | Eficiência Operacional", layout="wide")
st.title("📊 Dashboard Analítico - Eficiência Operacional Olist")

# Carregar dados
@st.cache_data
def load_data():
    conn = sqlite3.connect('olist.db')
    df = pd.read_sql("SELECT * FROM orders_consolidated", conn)
    conn.close()
    
    # Converter datas
    date_cols = ['order_purchase_timestamp', 'order_approved_at', 
                 'order_delivered_carrier_date', 'order_delivered_customer_date', 
                 'order_estimated_delivery_date']
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    
    return df

df = load_data()

# Filtros
col1, col2, col3 = st.columns(3)
with col1:
    selected_states = st.multiselect("Estados", 
                                   options=sorted(df['customer_state'].dropna().unique()), 
                                   default=['SP', 'RJ', 'MG', 'BA', 'RS', 'PR'])

with col2:
    date_min = df['order_purchase_timestamp'].min()
    date_max = df['order_purchase_timestamp'].max()
    selected_dates = st.date_input("Período", 
                                 [date_min.date() if pd.notnull(date_min) else pd.Timestamp('2016-01-01').date(), 
                                  date_max.date() if pd.notnull(date_max) else pd.Timestamp('2018-12-31').date()])

with col3:
    min_price, max_price = st.slider("Faixa de Preço (R$)", 
                                   float(df['price'].min() or 0), 
                                   float(df['price'].max() or 1000), 
                                   (0.0, 500.0))

# Filtragem
mask = (df['customer_state'].isin(selected_states)) & \
       (df['price'] >= min_price) & (df['price'] <= max_price)

if len(selected_dates) == 2:
    mask = mask & (df['order_purchase_timestamp'].dt.date >= selected_dates[0]) & \
                  (df['order_purchase_timestamp'].dt.date <= selected_dates[1])

df_filtered = df[mask].copy()

# KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de Pedidos", f"{len(df_filtered):,}")
col2.metric("Taxa de Atraso", f"{df_filtered['is_delayed'].mean():.1%}" if len(df_filtered) > 0 else "0%")
col3.metric("Ticket Médio", f"R$ {df_filtered['payment_value'].mean():.2f}" if len(df_filtered) > 0 else "R$ 0.00")
col4.metric("Acurácia do Modelo", "93.7%")

# Gráficos
st.subheader("📈 Taxa de Atraso por Estado")
fig1 = px.bar(df_filtered.groupby('customer_state')['is_delayed'].mean().reset_index().sort_values('is_delayed', ascending=False),
              x='customer_state', y='is_delayed', title="Atraso por Estado")
st.plotly_chart(fig1, use_container_width=True)

col_g1, col_g2 = st.columns(2)
with col_g1:
    st.subheader("Ticket Médio por Categoria (Top 10)")
    fig2 = px.bar(df_filtered.groupby('product_category_name')['payment_value'].mean().nlargest(10).reset_index(),
                  x='product_category_name', y='payment_value')
    st.plotly_chart(fig2, use_container_width=True)

with col_g2:
    st.subheader("Volume por Categoria (Top 8)")
    fig3 = px.pie(df_filtered.groupby('product_category_name').size().nlargest(8).reset_index(name='quantidade'),
                  names='product_category_name', values='quantidade')
    st.plotly_chart(fig3, use_container_width=True)

# Previsão de Atraso
st.subheader("🔮 Previsão de Atraso de Entrega")
with open('models/delay_model.pkl', 'rb') as f:
    model = pickle.load(f)

price = st.slider("Valor do Produto (R$)", 0, 2000, 150)
freight = st.slider("Valor do Frete (R$)", 0, 500, 40)
state = st.selectbox("Estado do Cliente", sorted(df['customer_state'].dropna().unique()))

if st.button("🔍 Prever Probabilidade de Atraso"):
    input_data = pd.DataFrame({
        'price': [price],
        'freight_value': [freight],
        'payment_value': [price + freight],
    })
    
    for col in model.feature_names_in_:
        if col.startswith('state_'):
            input_data[col] = 1 if col == f'state_{state}' else 0
    
    input_data = input_data.reindex(columns=model.feature_names_in_, fill_value=0)
    
    prob = model.predict_proba(input_data)[0][1]
    if prob > 0.5:
        st.error(f"⚠️ Alta probabilidade de atraso: **{prob:.1%}**")
    else:
        st.success(f"✅ Baixa probabilidade de atraso: **{prob:.1%}**")

st.caption("✅ Pipeline ETL + SQL + Random Forest (93.7% acurácia) | Projeto Portfólio")