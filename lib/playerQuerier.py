import sqlite3
from sqlite3 import Error

class PlayerQuerier():
    
    def __init__(self):
        self._pathToDb = "./db/players.db"
        self._conn =None

    def init(self):
        self._conn =self._connection(self._pathToDb)
        
    def _connection(self,db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)
            
        return conn
        
    def findPlayerIdByDetails(self,name,rating):
        cursor = self._conn.cursor()
        cursor.execute("SELECT * FROM players WHERE Name LIKE ? AND Rating LIKE ? ",("%"+name+"%","%"+rating+"%"))
        rows= cursor.fetchall()
        print(rows)
        


pq = PlayerQuerier()
pq.init()
pq.findPlayerIdByDetails(name="Neymar Jr",rating="96")