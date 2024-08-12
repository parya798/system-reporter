from flask import Flask, g
from memory.services import RamStatsService 
import sqlite3

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

DEFAULT_NUM_RECORDS = 1

@app.route("/last_ram_stats") 
def get_last_ram_stats_api(): 
    cursor = get_db().cursor() 
    return RamStatsService.get_last_ram_stats(cursor, DEFAULT_NUM_RECORDS)

@app.route("/biggest_app") 
def get_biggest_app_api(): 
    cursor = get_db().cursor() 
    return RamStatsService.get_biggest_app()