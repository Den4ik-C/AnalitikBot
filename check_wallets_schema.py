import sqlite3

conn = sqlite3.connect("crypto.db")
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(wallets)")
columns = cursor.fetchall()

print("📋 Колонки в таблице wallets:\n")
for col in columns:
    print(f"- {col[1]} (тип: {col[2]})")

conn.close()