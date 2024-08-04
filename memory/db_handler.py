import sqlite3 

class Database_memory: 
    def __init__(self, db_name): 
        self.connection = sqlite3.connect(db_name) 
        self.cursor = self.connection.cursor() 
        
    def get_connection(self): 
            return self.connection 
        
    def initialize_db(self): 
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS ram_stats (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, total REAL, free REAL, used REAL)''') 
            self.connection.commit() 
            
            
    def close_connection(self): 
            self.connection.close()