import pandas as pd
import sqlite3
import os
import glob

DATA_DIR = 'data'
DB_PATH = 'olist.db'

def find_file(pattern):
    files = glob.glob(os.path.join(DATA_DIR, f"*{pattern}*"))
    if files:
        print(f"✅ Encontrado: {os.path.basename(files[0])}")
        return files[0]
    raise FileNotFoundError(f"❌ Arquivo '{pattern}' não encontrado!")

def load_data():
    print("🔍 Carregando CSVs...")
    orders     = pd.read_csv(find_file("olist_orders_dataset"))
    items      = pd.read_csv(find_file("olist_order_items_dataset"))
    payments   = pd.read_csv(find_file("olist_order_payments_dataset"))
    customers  = pd.read_csv(find_file("olist_customers_dataset"))
    sellers    = pd.read_csv(find_file("olist_sellers_dataset"))
    products   = pd.read_csv(find_file("olist_products_dataset"))
    print("✅ Todos CSVs carregados!")
    return orders, items, payments, customers, sellers, products

def transform_data(orders, items, payments, customers, sellers, products):
    print("🔄 Aplicando transformações...")
    
    # Datas
    date_cols = ['order_purchase_timestamp', 'order_approved_at', 'order_delivered_carrier_date',
                 'order_delivered_customer_date', 'order_estimated_delivery_date']
    for col in date_cols:
        if col in orders.columns:
            orders[col] = pd.to_datetime(orders[col], errors='coerce')
    
    orders['delivery_delay'] = (orders['order_delivered_customer_date'] - orders['order_estimated_delivery_date']).dt.days
    orders['is_delayed'] = orders['delivery_delay'] > 0
    
    # Merge
    df = orders.merge(customers, on='customer_id', how='left')
    df = df.merge(items, on='order_id', how='left')
    df = df.merge(payments, on='order_id', how='left')
    df = df.merge(products, on='product_id', how='left')
    
    df['delivery_delay'] = df['delivery_delay'].fillna(999)
    df = df.fillna({'payment_value': 0, 'price': 0, 'freight_value': 0, 'product_category_name': 'Desconhecido'})
    
    print(f"📊 Dataset final: {df.shape[0]:,} linhas e {df.shape[1]} colunas")
    return df

def save_to_sqlite(df):
    try:
        conn = sqlite3.connect(DB_PATH)
        df.to_sql('orders_consolidated', conn, if_exists='replace', index=False)
        size_mb = os.path.getsize(DB_PATH) / (1024*1024)
        print(f"💾 Banco salvo com sucesso! ({size_mb:.1f} MB)")
        conn.close()
    except Exception as e:
        print(f"❌ Erro ao salvar no SQLite: {e}")

if __name__ == "__main__":
    try:
        orders, items, payments, customers, sellers, products = load_data()
        df = transform_data(orders, items, payments, customers, sellers, products)
        save_to_sqlite(df)
        print("\n🎉 ETL FINALIZADO!")
    except Exception as e:
        print(f"\n❌ ERRO GERAL: {e}")