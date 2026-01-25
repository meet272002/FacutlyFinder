from fastapi import FastAPI
from dbConnection.db_connection import SQLConnection as sc
from dbOperations.get_data import GetData
from contextlib import closing

app = FastAPI()

@app.get("/faculty")
def get_faculty_data():
    data = {}
    connection = sc().getConnection()
    connection_status = connection[1]
    if connection_status != 1:
        data = {"error":"Database connection failed"}
    else:
        with closing(sc().getConnection()[0]) as conn:
            data_getter = GetData(conn)
            data = data_getter.get_data()
    return {"data": data}
