import streamlit as st
import requests
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="Faculty Matcher", layout="wide")

class FacultyRecommender:
    def __init__(self, api_url):
        self.api_url = api_url
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def fetch_data(self):
        try:
            response = requests.get(f"{self.api_url}/faculty")
            return response.json()['data']
        except:
            return []

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

st.title("Faculty Recommendation System")
st.markdown("Enter your interests below to find the most relevant faculty members for your research or studies.")

with st.sidebar:
    st.header("Search Parameters")
    user_input = st.text_area("Your Interests", placeholder="e.g. Machine Learning, Cyber Security, Blockchain...")
    num_rec = st.slider("Number of recommendations", 1, 10, 5)
    find_btn = st.button("Find Matches", type="primary")

recommender = FacultyRecommender("http://127.0.0.1:8000")
data = recommender.fetch_data()

if find_btn and user_input:
    if not data:
        st.error("Could not connect to the Faculty API. Please ensure your FastAPI server is running.")
    else:
        results = recommender.recommend(user_input, data, top_n=num_rec)
        
        if not results:
            st.warning("No close matches found. Try using different keywords.")
        else:
            st.subheader(f"Top {len(results)} Faculty Matches")
            
            for faculty, score in results:
                with st.expander(f"{faculty['Name']} - {int(score*100)}% Match"):
                        st.write("**Specialization:**")
                        st.caption(", ".join(faculty.get("Specializations", [])))
                        st.write("**Current Research:**")
                        st.caption(", ".join(faculty.get("Researches", [])))

elif not find_btn:
    st.info("Enter your preferences in the sidebar and click 'Find Matches'.")