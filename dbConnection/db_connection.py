import sqlite3
import os
from pathlib import Path


class SQLConnection:
    def __init__(self):
        self.BASE_DIR = Path(__file__).resolve().parent
        self.DATA_DIR = self.BASE_DIR.parent / "database"
        self.dbPath = self.DATA_DIR / 'faculty_managment.db'

    def getConnection(self):
        try:
            os.makedirs(self.DATA_DIR, exist_ok=True)
            conn = sqlite3.connect(self.dbPath)
            return (conn,1)
        except Exception as e:
            return (None,0)
