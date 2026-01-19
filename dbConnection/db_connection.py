import sqlite3
import os

class SQLConnection:
    def __init__(self):
        self.dbPath = 'data/faculty_managment.db'

    def getConnection(self):
        os.makedirs("data", exist_ok=True)
        return sqlite3.connect(self.dbPath)