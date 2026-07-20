from contextlib import closing
from fastapi import APIRouter, HTTPException, Query

router = APIRouter(prefix="/search", tags=["search"])

# Import your database connection
from server.dbConnection.db_connection import SQLConnection as sc
from server.dbOperations.get_data import GetData
import server.state as state

@router.get("/faculty")
def get_faculty_data(query: str = Query(..., description="User query for faculty recommendation"),top_n: int = Query(5, ge=1, le=10)):
    try:
        data = {}
        connection = sc().getConnection()
        connection_status = connection[1]

        if connection_status != 1:
            data = {"error":"Database connection failed"}
        else:
            with closing(connection[0]) as conn:
                data_getter = GetData(conn)
                data = data_getter.get_data()
        
        results = state.recommender_instance.recommend(            
                user_query=query,
                faculty_data=data,
                top_n=top_n)
        converted_results = []
        for item in results:
            converted_item = {
                'name': str(item[0].get('Name', 'N/A')),
                'email': str(item[0].get('Email', 'N/A')),
                'specializations': [str(spec) for spec in item[0].get('Specializations', [])],
                'researches': [str(res) for res in item[0].get('Researches', [])],
                'similarity': float(item[1])  # ✅ Convert numpy.float32 to float
            }
            converted_results.append(converted_item)
        return {"success": True, "query": query, "results": converted_results}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
