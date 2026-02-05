import streamlit as st
import requests

st.set_page_config(page_title="Faculty Matcher", layout="wide")

API_URL = "https://facutlyfinder-backend.onrender.com"

st.title("Faculty Recommendation System")
st.markdown("Enter your interests to find relevant faculty members.")

with st.sidebar:
    user_input = st.text_area(
        "Your Interests",
        placeholder="Machine Learning, Cyber Security, Blockchain..."
    )
    num_rec = st.slider("Number of recommendations", 1, 10, 5)
    find_btn = st.button("Find Matches", type="primary")

if find_btn and user_input:
    with st.spinner("Finding best matches..."):
        response = requests.post(
            f"{API_URL}/recommend",
            json={"query": user_input, "top_n": num_rec},
            timeout=30
        )

    if response.status_code != 200:
        st.error("Backend error")
    else:
        results = response.json()["results"]

        if not results:
            st.warning("No close matches found.")
        else:
            st.subheader(f"Top {len(results)} Faculty Matches")
            for r in results:
                faculty = r["faculty"]
                score = int(r["score"] * 100)

                with st.expander(f"{faculty['Name']} — {score}% match"):
                    st.write("**Specialization:**")
                    st.caption(", ".join(faculty.get("Specializations", [])))
                    st.write("**Research:**")
                    st.caption(", ".join(faculty.get("Researches", [])))
else:
    st.info("Enter preferences and click *Find Matches*.")
