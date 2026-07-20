"""
FastAPI routes for Faculty Comparison Tool.
Add these routes to your existing FastAPI.py file.

Usage:
------
In your FastAPI.py, add:
    from comparison.fastapi_routes import router
    app.include_router(router)
"""

from contextlib import closing

from fastapi import APIRouter, HTTPException, Query
from typing import List
import sqlite3

import server.state as state

router = APIRouter(prefix="/compare", tags=["comparison"])

# Import your database connection
from server.dbConnection.db_connection import SQLConnection as sc
from server.comparison.compare import FacultyComparator
from server.dbOperations.get_data import GetData

@router.get("/get_faculty")
async def get_faculty():
    """
    Get Faculty faculty by their IDs.
    
    Returns:
        All Faculty Details
    """
    try:
        conn = sc().getConnection()[0]
        cursor = conn.cursor()
        data = {}
        connection_status = sc().getConnection()[1]
        
        if connection_status != 1:
            data = {"error":"Database connection failed"}
        else:
            with closing(sc().getConnection()[0]) as conn:
                data_getter = GetData(conn)
                data = data_getter.get_data()        
        conn.close()
        return {"status": "success", "data": data}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid faculty IDs format. Use comma-separated numbers.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/faculty/{faculty_ids}")
async def compare_faculty(faculty_ids: str):
    """
    Compare multiple faculty by their IDs.
    
    Args:
        faculty_ids: Comma-separated faculty IDs (e.g., "1,2,3")
    
    Returns:
        Comprehensive comparison report with specializations, teaching areas, education, research
    """
    try:
        ids = [int(id.strip()) for id in faculty_ids.split(',')]
        conn = sc().getConnection()[0]
        cursor = conn.cursor()

        data = {}
        connection_status = sc().getConnection()[1]
        
        if connection_status != 1:
            data = {"error":"Database connection failed"}
        else:
            with closing(sc().getConnection()[0]) as conn:
                data_getter = GetData(conn)
                data = data_getter.get_faculty_by_ids(ids)
        report = state.comparator_instance.generate_comparison_report(data)
        conn.close()
        return {"status": "success", "data": report}
    
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid faculty IDs format. Use comma-separated numbers.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    