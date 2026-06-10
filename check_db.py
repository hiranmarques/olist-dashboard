import sqlite3
import os

print("🔍 Verificando banco de dados...\n")

if not os.path.exists('olist.db'):
    print("❌ Arquivo 'olist.db' NÃO encontrado!")
    print("   Rode o ETL novamente.")
else:
    print(f"✅ Banco encontrado ({os.path.getsize('olist.db') / (1024*1024):.1f} MB)")
    
    conn = sqlite3.connect('olist.db')
    tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    
    print("\n📋 Tabelas encontradas:")
    for table in tables:
        print(f"   → {table[0]}")
    
    # Verifica quantidade de linhas
    try:
        count = conn.execute("SELECT COUNT(*) FROM orders_consolidated").fetchone()[0]
        print(f"\n📊 orders_consolidated tem {count:,} registros")
    except:
        print("   Tabela orders_consolidated não encontrada!")
    
    conn.close()