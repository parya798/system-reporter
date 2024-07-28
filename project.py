from flask import Flask, jsonify,request
import sqlite3
import psutil
from datetime import datetime
from threading import Timer


app = Flask(__name__)
db_name = "ram_stats.db"

class ramStatsRecorder:
    def __init__(self):
        self.conn = sqlite3.connect(db_name)
        self.c = self.conn.cursor()
        self.create_table()
        self.record_ram_stats()
    
        
    def create_table(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS ram_stats 
                       (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       timestamp TIMESTAMP, total REAL, free REAL, used REAL)''')
        self.conn.commit()
        


    def record_ram_stats(self):
        total_ram = psutil.virtual_memory().total / (1024*1024)
        free_ram = psutil.virtual_memory().free / (1024*1024)
        used_ram = psutil.virtual_memory().used / (1024*1024)
        timestamp = datetime.now()
    
        self.c.execute("INSERT INTO ram_stats(timestamp, total, free, used) VALUES (?,?,?,?)",
        (timestamp, total_ram, free_ram, used_ram))
        self.conn.commit()
    
    
        t = Timer(60.0, self.record_ram_stats)
        t.start()
    
    
class ramStatsAPI:
    def __init__(self):
        self.conn = sqlite3.connect(db_name)
        self.c = self.conn.cursor()
        
    def get_last_ram_stats(self):
        num_records = int(request.args.get("num_records", 10))
        
        self.c.execute("SELECT * FROM ram_stats ORDER BY timestamp DESC LIMIT ?", 
                       (num_records,))
        records = self.c.fetchall()
        
        result = []
        for record in records:
            result.append({
               "timestamp": record[1],
               "total": record [2],
               "free": record [3],
               "used": record [4]
            })
            
        return jsonify(result)
    
ram_stats_recorder = ramStatsRecorder()
ram_stats_api = ramStatsAPI()


@app.route("/last_ram_stats", methods=["GET"])
def get_last_ram_stats():
    return ram_stats_api.get_last_ram_stats()
    
    
if __name__ == "__main__":
    app.run()
    
    
    
    