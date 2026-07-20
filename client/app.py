import streamlit as st
import requests

st.set_page_config(page_title="Advisor Matcher", layout="wide")
st.title("Advisor Matching Platform")

# Add navigation in sidebar
page = st.sidebar.radio(
    "Navigation",
    ["Search Faculty", "Compare Faculty"],
    help="Switch between searching and comparing faculty"
)

st.markdown("---")

API_BASE = "http://localhost:8005"

if page == "Search Faculty":
    st.markdown("Enter your interests below to find the most relevant faculty members for your research or studies.")

    with st.sidebar:
        st.header("Search Parameters")
        user_input = st.text_area(
            "Your Interests",
            placeholder="e.g. Machine Learning, Cyber Security, Blockchain..."
        )
        num_rec = st.slider("Number of recommendations", 1, 10, 5)
        find_btn = st.button("Find Matches", type="primary")

    if find_btn and user_input:
        try:
            resp = requests.get(
                f"{API_BASE}/search/faculty",
                params={"query": user_input, "top_n": num_rec},
                timeout=30,
            )
        except requests.exceptions.RequestException:
            st.error("Could not reach the Faculty API. Is the FastAPI server running?")
        else:
            if resp.status_code != 200:
                st.error(f"API error {resp.status_code}: {resp.text}")
            else:
                results = resp.json().get("results", [])

                if not results:
                    st.warning("No close matches found. Try using different keywords.")
                else:
                    st.subheader(f"Top {len(results)} Faculty Matches")
                    for faculty in results:
                        score = faculty.get("similarity", 0)
                        with st.expander(f"{faculty['name']} — {int(score * 100)}% Match"):
                            st.write("**Email:**")
                            st.caption(faculty.get("email", "N/A"))
                            st.write("**Specialization:**")
                            st.caption(", ".join(faculty.get("specializations", [])) or "N/A")
                            st.write("**Current Research:**")
                            st.caption(", ".join(faculty.get("researches", [])) or "N/A")

    elif not find_btn:
        st.info("Enter your preferences in the sidebar and click 'Find Matches'.")
elif page == "Compare Faculty":
    st.markdown("Select 2-5 faculty members to compare their profiles, research interests, and specializations.")
    
    # Fetch all faculty for dropdown
    try:
        response = requests.get(f"{API_BASE}/compare/get_faculty")  # Adjust URL if needed
        if response.status_code == 200:
            all_faculty = response.json().get('data', [])
            faculty_dict = {f['Name']: f['Faculty_id'] for f in all_faculty}
            
            # Multi-select dropdown
            selected_names = st.multiselect(
                "Choose 2-5 faculty members to compare",
                options=list(faculty_dict.keys()),
                max_selections=5,
                help="Select multiple faculty to compare their profiles"
            )
            
            if len(selected_names) >= 2:
                selected_ids = [faculty_dict[name] for name in selected_names]
                
                # Call FastAPI comparison endpoint
                ids_str = ','.join(map(str, selected_ids))
                comp_response = requests.get(f"{API_BASE}/compare/faculty/{ids_str}")
                
                if comp_response.status_code == 200:
                    comparison_data = comp_response.json().get('data', {})
                    
                    report = comparison_data

                    if 'error' in report:
                        st.warning(report['error'])
                        st.stop()

                    # ── Faculty profile cards ─────────────────────────────────────
                    st.subheader("Faculty Profiles")

                    faculties = report.get('faculty', [])
                    spec_by_faculty = report.get('specialization_comparison', {}).get('by_faculty', {})
                    edu_by_faculty = report.get('education_comparison', {}).get('by_faculty', {})

                    profile_cols = st.columns(len(faculties))
                    for col, faculty in zip(profile_cols, faculties):
                        with col:
                            name = faculty['name']
                            st.markdown(f"### {name}")

                            degree = edu_by_faculty.get(name)
                            if degree and degree != 'N/A':
                                st.caption(degree)

                            st.divider()

                            specs = spec_by_faculty.get(name, [])
                            if specs:
                                st.markdown("**Specializations:**")
                                for s in specs[:5]:
                                    st.caption(f"• {s}")
                                if len(specs) > 5:
                                    st.caption(f"_+{len(specs) - 5} more_")
                            else:
                                st.caption("_No specializations listed_")

                    st.divider()

                    # ── Overall similarity ────────────────────────────────────────
                    st.subheader("Comparison Analysis")

                    overall = report.get('overall_similarity', {})
                    for pair, vals in overall.items():
                        st.metric(pair, f"{vals['overall_score']}%")
                        breakdown_cols = st.columns(4)
                        for bcol, (dim, val) in zip(breakdown_cols, vals['breakdown'].items()):
                            bcol.caption(dim.title())
                            bcol.write(f"**{val}%**")
                        st.divider()


                    # ── Per-dimension detail ──────────────────────────────────────
                    def render_dimension(title, section):
                        if not section or not section.get('pairwise'):
                            return

                        st.subheader(title)
                        for pair, vals in section['pairwise'].items():
                            st.markdown(f"**{pair}** — {round(vals['score'] * 100, 1)}%")

                            exact = vals.get('exact_matches', [])
                            st.write(f"Shared: {', '.join(exact)}" if exact else "No exact matches")

                            for s in vals.get('similar_pairs', []):
                                st.caption(f"{s['from']} ≈ {s['to']} ({round(s['similarity'] * 100)}%)")
                        st.divider()


                    render_dimension("Specializations", report.get('specialization_comparison'))
                    render_dimension("Research Interests", report.get('research_comparison'))
                    render_dimension("Teaching Areas", report.get('teaching_comparison'))

                    # ── Education ─────────────────────────────────────────────────
                    edu = report.get('education_comparison', {})
                    if edu.get('pairwise'):
                        st.subheader("Education")
                        for pair, vals in edu['pairwise'].items():
                            tag = " — same degree" if vals.get('same_degree') else ""
                            st.write(f"{pair}: {round(vals['score'] * 100, 1)}%{tag}")
                else:
                    st.error("Error fetching comparison data from server")
            
            elif len(selected_names) > 0:
                st.warning("Please select at least 2 faculty members to compare")
            else:
                st.info("Select faculty members from the dropdown above")
                
        else:
            st.error("Could not load faculty list")
            
    except Exception as e:
        st.error(f"Error: {e}")