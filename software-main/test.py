import pyodbc

# 這是最原始、沒有經過 Django 包裝的連線字串 (注意 IP 和 Port 中間是逗號)
conn_str = (
    "Driver={ODBC Driver 18 for SQL Server};"
    "Server=127.0.0.1,1433;"
    "Database=classroom;"
    "UID=sa;"
    "PWD=01257014;"
    "Encrypt=no;"
    "TrustServerCertificate=yes;"
)

try:
    print("嘗試連線中...")
    conn = pyodbc.connect(conn_str, timeout=3)
    print("✅ 連線成功！資料庫與網路設定完全沒問題。")
    conn.close()
except Exception as e:
    print("❌ 連線失敗：")
    print(e)