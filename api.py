from flask import Flask, request, g 
from services import RamStatsService 
from db_handler import Database_memory 

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
    
@app.route("/last_ram_stats") 
def get_last_ram_stats_api(): 
    num_records = int(request.args.get("num_records", 10)) 
    cursor = get_db().cursor() 
    return RamStatsService.get_last_ram_stats(cursor, num_records)