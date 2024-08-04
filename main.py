from memory.db_handler import Database_memory
from memory.services import RamStatsService 
from memory.api import db_name, app

db = Database_memory(db_name)

db.initialize_db()

RamStatsService.record_ram_stats(db_name)

app.run("0.0.0.0", 3000)