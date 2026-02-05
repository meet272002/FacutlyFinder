from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dbConnection.db_connection import SQLConnection as sc
from dbOperations.get_data import GetData
from contextlib import closing
import subprocess
import sys

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501",
        "https://facutlyfinder-dduo.onrender.com",
        "https://facutlyfinder-5tnqrfu5mpkdwkvppg2f3x.streamlit.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.get("/")
def read_root():
    return {"status": "Server is running 🚀"}
