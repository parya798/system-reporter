from flask import Flask, jsonify,request
import sqlite3
import psutil
from datetime import datetime
from threading import Timer


app = Flask(__name__)
db_name = "ram_stats.db"

def record_ram_stats():
    total_ram = psutil.virtual_memory().total / (1024*1024)
    free_ram = psutil.virtual_memory().free /(1024*1024)
    used_ram = psutil.virtual_memory().used / (1024*1024)
    timestamp = datetime.now()
    
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("INSERT INTO ram_stats (timestamp, total, free, used) VALUES (?,?,?,?)",
              (timestamp, total_ram, free_ram, used_ram))
    conn.commit()
    conn.close()
    
    t = Timer(60.0, record_ram_stats)
    t.start()
    
@app.route("/last_ram_stats", methods = ["GET"])
def get_last_ram_stats():
    num_records = int(request.args.get("num_records", 10))
    
    conn = sqlite3.connect(db_name)
    c= conn.cursor()
    c.execute("SELECT * FROM ram_stats ORDER BY timestamp DESC LIMIT ?", (num_records,))
    records = c.fetchall()
    conn.close()
    
    result = []
    for record in records:
        result.append({
            "timestamp": record[1],
        "total": record [2],
        "free": record [3],
        "used": record [4]
        })
    return jsonify(result)

if __name__ == "__main__":
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS ram_stats 
              (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TIMESTAMP, 
              total REAL, free REAL, used REAL)''')
    conn.close()
    
    record_ram_stats()
    app.run()
    
    
    
    