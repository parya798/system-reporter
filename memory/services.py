import sqlite3
import psutil 
from datetime import datetime 
from threading import Timer 
from flask import jsonify 

class RamStatsService: 
        @staticmethod 
        #this func inserts RAM stats into database and schedules itself to run every 60s
        def record_ram_stats(db_name):
                connection = sqlite3.connect(db_name) 
                cursor = connection.cursor() 
                
                timestamp = datetime.now() 
                ram_info = psutil.virtual_memory() 
                total_ram = ram_info.total / (1024 * 1024) 
                free_ram = ram_info.free / (1024 * 1024) 
                used_ram = ram_info.used / (1024 * 1024) 
                
                cursor.execute("INSERT INTO ram_stats(timestamp, total, free, used) VALUES (?,?,?,?)", 
                                (timestamp, total_ram, free_ram, used_ram)) 
                connection.commit() 
                print("Stats saved") 
                
                t = Timer(60, lambda: RamStatsService.record_ram_stats(db_name)) 
                t.start() 
                        
                
        @staticmethod 
        #fetches the last 'n' RAM stats records from database and returns them as a JSON
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
                
        @staticmethod 
        #finds the process with the highest memory usage and returns it as JSON
        def get_biggest_app(): 
                processes = {p.pid: p.info for p in psutil.process_iter(['pid', 'name', 'memory_info'])} 
                biggest_app = max(processes.values(), key=lambda x: x['memory_info'].rss) 
                        
                return jsonify({"name": biggest_app['name'], "memory_usage_mb": biggest_app['memory_info'].rss / (1024 * 1024)})