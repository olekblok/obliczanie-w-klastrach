import os
import happybase
from flask import Flask, jsonify

HBASE_HOST = os.getenv("HBASE_HOST", "localhost")
HBASE_PORT = int(os.getenv("HBASE_PORT", "9090"))
TABLE_NAME = "etf_data"

app = Flask(__name__)

def get_connection():
    return happybase.Connection(host=HBASE_HOST, port=HBASE_PORT)

@app.route('/etf/<symbol>', methods=['GET'])
def get_etf_data(symbol):
    conn = get_connection()
    table = conn.table(TABLE_NAME)
    rows = table.scan(row_prefix=symbol.encode())
    
    result = []
    for key, data in rows:
        record = {k.decode(): v.decode() for k, v in data.items()}
        record['row_key'] = key.decode()
        result.append(record)
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
