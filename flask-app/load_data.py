import happybase
import os

HBASE_HOST = os.environ.get("HBASE_HOST", "localhost")
ETF_DIR = "./ETFs"

def connect():
    conn = happybase.Connection(HBASE_HOST)
    conn.open()
    return conn

def ensure_table(conn):
    if b'etf_data' not in conn.tables():
        conn.create_table('etf_data', {'data': dict()})
        print("Created 'etf_data' table.")

def load_data():
    conn = connect()
    ensure_table(conn)
    table = conn.table('etf_data')

    for filename in os.listdir(ETF_DIR):
        if filename.endswith(".txt"):
            symbol = filename.replace(".txt", "")
            filepath = os.path.join(ETF_DIR, filename)

            with open(filepath, "r") as f:
                lines = f.readlines()[1:]  # Skip header
                for line in lines:
                    fields = line.strip().split(",")
                    if len(fields) != 7:
                        continue
                    date, open_, high, low, close, volume, openint = fields
                    row_key = f"{symbol}_{date}"
                    table.put(row_key, {
                        b"data:symbol": symbol.encode(),
                        b"data:date": date.encode(),
                        b"data:open": open_.encode(),
                        b"data:high": high.encode(),
                        b"data:low": low.encode(),
                        b"data:close": close.encode(),
                        b"data:volume": volume.encode(),
                        b"data:openint": openint.encode(),
                    })
            print(f"Loaded {filename}")
    conn.close()

if __name__ == "__main__":
    load_data()
