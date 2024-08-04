from db_handler import Database_memory
import psutil 
from datetime import datetime 
from threading import Timer 
from flask import jsonify 
import sqlite3

class RamStatsService: 
        @staticmethod 
        def record_ram_stats(db_name):
                connection = sqlite3.connect(db_name) 
                cursor = connection.cursor() 
                
                def record_stats(): 
                        timestamp = datetime.now() 
                        ram_info = psutil.virtual_memory() 
                        total_ram = ram_info.total / (1024 * 1024) 
                        free_ram = ram_info.free / (1024 * 1024) 
                        used_ram = ram_info.used / (1024 * 1024) 
                        
                        cursor.execute("INSERT INTO ram_stats(timestamp, total, free, used) VALUES (?,?,?,?)", 
                                       (timestamp, total_ram, free_ram, used_ram)) 
                        connection.commit() 
                        print("Stats saved") 
                        
                        t = Timer(60, record_stats) 
                        t.start() 
                        
                record_stats()
                
        @staticmethod 
        def get_last_ram_stats(cursor, num_records): 
            cursor.execute("SELECT * FROM ram_stats ORDER BY timestamp DESC LIMIT ?", (num_records,)) 
            records = cursor.fetchall() 
                
            result = [] 
            for record in records: 
                result.append({ 
                    "timestamp": record[1], 
                    "total": record[2], 
                    "free": record[3], 
                    "used": record[4] 
                    }) 
                        
            return jsonify(result)