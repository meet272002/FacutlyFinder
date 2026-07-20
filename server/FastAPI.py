from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import SentenceTransformer
from server.comparison.compare import FacultyComparator
from server.comparison.fastapi_routes import router as comparison_router
from server.search.fastapi_routes import router as search_router
from server.search.search import FacultyRecommender
import server.state as state

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Loading models on startup...")
    state.loaded_model = SentenceTransformer('paraphrase-MiniLM-L3-v2')
    print("Sentence Transformer model loaded")
    
    state.recommender_instance = FacultyRecommender()
    state.recommender_instance.model = state.loaded_model

    state.comparator_instance = FacultyComparator()
    state.comparator_instance.model = state.loaded_model
    
    print("Recommender initialized")
    
    yield

    print("Cleaning up resources...")
    state.loaded_model = None
    state.recommender_instance = None
    state.comparator_instance = None

app = FastAPI(lifespan=lifespan)
    
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

app.include_router(comparison_router)
app.include_router(search_router)

@app.get("/")
def read_root():
    return {"status": "Server is running 🚀"}
