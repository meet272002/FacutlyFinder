from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import requests

class FacultyRecommender:
    def __init__(self):
        self.model = SentenceTransformer('paraphrase-MiniLM-L3-v2', device="cpu")

    def recommend(self, user_query, faculty_data, top_n=3):
        profiles = [
            " ".join(f.get("Specializations", []) + f.get("Teachings", []) + f.get("Researches", [])).lower()
            for f in faculty_data
        ]

        faculty_embeddings = self.model.encode(profiles)
        user_embedding = self.model.encode([user_query.lower()])

        scores = cosine_similarity(user_embedding, faculty_embeddings).flatten()
        
        top_indices = scores.argsort()[-top_n:][::-1]
        return [(faculty_data[i], scores[i]) for i in top_indices if scores[i] > 0]