from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from dbConnection.db_connection import SQLConnection as sc
from dbOperations.get_data import GetData
from contextlib import closing

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

model = SentenceTransformer("all-MiniLM-L6-v2")

def get_faculty():
    conn, status = sc().getConnection()
    if status != 1:
        return []
    with closing(conn):
        return GetData(conn).get_data()

@app.get("/")
def read_root():
    return {"status": "Server is running"}

@app.get("/faculty")
def faculty():
    return {"data": get_faculty()}

@app.post("/recommend")
def recommend(payload: dict):
    query = payload["query"].lower()
    top_n = payload.get("top_n", 5)

    faculty = get_faculty()
    if not faculty:
        return {"results": []}

    profiles = [
        " ".join(
            f.get("Specializations", []) +
            f.get("Teachings", []) +
            f.get("Researches", [])
        ).lower()
        for f in faculty
    ]

    faculty_emb = model.encode(profiles)
    query_emb = model.encode([query])

    scores = cosine_similarity(query_emb, faculty_emb).flatten()
    top_idx = scores.argsort()[-top_n:][::-1]

    results = [
        {"faculty": faculty[i], "score": float(scores[i])}
        for i in top_idx if scores[i] > 0
    ]

    return {"results": results}
