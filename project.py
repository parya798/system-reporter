from flask import Flask, jsonify, request, g
import sqlite3
import psutil
from datetime import datetime
from threading import Timer


app = Flask(__name__)
db_name = "ram_stats.db"

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(db_name)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

class RamStatsService:
    def create_table(cur):
        cur.execute('''CREATE TABLE IF NOT EXISTS ram_stats 
                        (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        timestamp TIMESTAMP, total REAL, free REAL, used REAL)''')

    def record_ram_stats(cur):
        total_ram = psutil.virtual_memory().total / (1024 * 1024)
        free_ram = psutil.virtual_memory().free / (1024 * 1024)
        used_ram = psutil.virtual_memory().used / (1024 * 1024)
        timestamp = datetime.now()
    
        cur.execute("INSERT INTO ram_stats(timestamp, total, free, used) VALUES (?,?,?,?)",
        (timestamp, total_ram, free_ram, used_ram))

    def get_last_ram_stats(cur, num_records):
        cur.execute("SELECT * FROM ram_stats ORDER BY timestamp DESC LIMIT ?", 
                       (num_records,))
        records = cur.fetchall()
        
        result = []
        for record in records:
            result.append({
               "timestamp": record[1],
               "total": record [2],
               "free": record [3],
               "used": record [4]
            })
        
        return jsonify(result)
    
@app.route("/last_ram_stats")
def get_last_ram_stats():
    num_records = int(request.args.get("num_records", 10))
    cur = get_db().cursor()
    return RamStatsService.get_last_ram_stats(cur, num_records)
    
if __name__ == "__main__":
    cur = get_db().cursor()

    RamStatsService.create_table(cur)
    RamStatsService.record_ram_stats(cur)

    t = Timer(60.0, lambda: RamStatsService.record_ram_stats(cur))
    t.start()
    
    app.run()