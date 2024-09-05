from flask import Flask, g
from memory.services import RamStatsService 
import sqlite3
from pydantic import BaseModel, Field
from flask_pydantic import validate


app = Flask(__name__) 
db_name = "ram_stats.db" 

#gets a database connection
def get_db(): 
    db = getattr(g, '_database', None) 
    if db is None: 
        db = g._database = sqlite3.connect(db_name) 
    return db 

#closes the database connection after the apllication context ends
@app.teardown_appcontext 
def close_connection(exception): 
    db = getattr(g, '_database', None) 
    if db is not None: 
       db.close() 

class LastRamStatsQueryParams(BaseModel):
    num_records: int = Field(default=5, description="Number of records to retrieve")
    
    
@app.route("/last_ram_stats")
@validate()
def get_last_ram_stat_api(query: LastRamStatsQueryParams):
    cursor = get_db().cursor()
    return RamStatsService.get_last_ram_stats(cursor, query.num_records) 



@app.route("/biggest_app") 
def get_biggest_app_api(): 
    print("done")
    return RamStatsService.get_biggest_app()