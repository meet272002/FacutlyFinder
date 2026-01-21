import sqlite3
import os
from pathlib import Path

class SQLConnection:
    def __init__(self):
        self.BASE_DIR = Path(__file__).resolve().parent
        self.DATA_DIR = self.BASE_DIR.parent / "database"
        self.dbPath = self.DATA_DIR / 'faculty_managment.db'

    def getConnection(self):
        os.makedirs(self.DATA_DIR, exist_ok=True)
        conn =  sqlite3.connect(self.dbPath)
        if conn:
           return (conn,1)
        else:
            return (conn,0)
