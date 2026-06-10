import pandas as pd
import sqlite3
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle
import os

print("🔄 Carregando dados do banco...")

conn = sqlite3.connect('olist.db')
df = pd.read_sql("SELECT * FROM orders_consolidated LIMIT 80000", conn)
conn.close()

print(f"✅ Dados carregados: {df.shape[0]:,} linhas")

# Preparação para o modelo
features = ['price', 'freight_value', 'payment_value']
df_model = df[features + ['is_delayed', 'customer_state']].copy()

# One-hot encoding para estado
df_model = pd.get_dummies(df_model, columns=['customer_state'], prefix='state')

X = df_model.drop('is_delayed', axis=1)
y = df_model['is_delayed']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("🤖 Treinando Random Forest...")
model = RandomForestClassifier(n_estimators=100, max_depth=12, random_state=42, n_jobs=-1)
model.fit(X_train, y_train)

pred = model.predict(X_test)
accuracy = accuracy_score(y_test, pred)

print(f"🎯 Acurácia: {accuracy:.1%}")

# Salvar modelo
with open('models/delay_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("💾 Modelo salvo com sucesso!")