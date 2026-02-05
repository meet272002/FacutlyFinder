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
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def run_system_tasks():
    try:
        process = subprocess.Popen(
                    [sys.executable, "-m", "scrape.dau.main"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1  # Line buffered
                )

        process.wait()  # Wait for it to officially finish

        if process.returncode == 0:
            return {"status": "success", "message": "Data loaded successfully"}
        else:
            raise HTTPException(status_code=500, detail="Scraper failed")
    except subprocess.CalledProcessError as e:
        print(f"Error during tasks: {e}")

def run_system_database():
    try:
        print("--- Initializing Database ---")
        
        # subprocess.Popen allows us to stream the output
        process = subprocess.Popen(
            [sys.executable, "main.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1 # Line buffered for immediate log printing
        )

        process.wait() # Ensure the process has finished

        if process.returncode == 0:
            return {
                "status": "success", 
                "message": "Database initialized and data loaded successfully."
            }
        else:
            raise HTTPException(
                status_code=500, 
                detail=f"Database script failed with return code {process.returncode}"
            )
    except subprocess.CalledProcessError as e:
        print(f"Error during tasks: {e}")

@app.get("/run-tasks")
def trigger_tasks():
    result = run_system_tasks() 
    return {"status": "Scraper completed.", "details": result}

@app.get("/run-tasks-database")
def trigger_tasks_database():
    result = run_system_database() 
    return {"status": "Scraper completed.", "details": result}


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
