import streamlit as st
import pandas as pd
import plotly.express as px

from backend.parser import (
    extract_text_from_pdf,
    extract_text_from_docx,
    extract_contact_info,
    extract_experience
)

from backend.skills import extract_skills
from backend.matcher import compute_match_score
from backend.database import save_candidate


# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Smart Hire Analyzer", layout="wide")


# ---------------- CSS ----------------
def load_css():
    with open("frontend/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()


# ---------------- HEADER ----------------
st.markdown("""
<h1>Smart Hire Analyzer</h1>
<p style='text-align:center;color:#94a3b8'>
AI-Powered Resume Screening System
</p>
""", unsafe_allow_html=True)

st.markdown("---")


# ---------------- INPUT ----------------
uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])
job_description = st.text_area("Paste Job Description")

analyze = st.button("Analyze Resume")


# ---------------- PROCESS ----------------
if analyze:

    if not uploaded_file:
        st.warning("Upload resume first")
        st.stop()

    if not job_description:
        st.warning("Enter job description")
        st.stop()

    # Extract text
    if uploaded_file.type == "application/pdf":
        text = extract_text_from_pdf(uploaded_file)
    else:
        text = extract_text_from_docx(uploaded_file)

    # Extract data
    info = extract_contact_info(text)
    skills = extract_skills(text)
    experience = extract_experience(text)

    keyword_score = compute_match_score(text, job_description)

    skills_score = min(len(skills) * 12, 100)
    experience_score = min(int(experience) * 10, 100)

    # FINAL SCORE (improved logic)
    final_score = round(
        (0.5 * skills_score) +
        (0.2 * experience_score) +
        (0.3 * keyword_score),
        2
    )

    # Save to DB
    save_candidate({
        "name": info["name"],
        "email": info["email"],
        "phone": info["phone"],
        "skills": ", ".join(skills),
        "experience": experience,
        "score": final_score
    })

    # Store session data
    st.session_state.data = {
        "info": info,
        "skills": skills,
        "experience": experience,
        "skills_score": skills_score,
        "experience_score": experience_score,
        "keyword_score": keyword_score,
        "final_score": final_score
    }

    st.success("Analysis Complete!")


# ---------------- OUTPUT ----------------
if "data" in st.session_state:

    d = st.session_state.data

    st.markdown("## Candidate Report")

    st.write(d["info"])

    st.markdown("## Scores")

    st.metric("Final ATS Score", f"{d['final_score']}%")
    st.metric("Skills Score", d["skills_score"])
    st.metric("Experience Score", d["experience_score"])
    st.metric("Keyword Score", d["keyword_score"])

    st.markdown("## Skills")

    for s in d["skills"]:
        st.markdown(f"✔ {s}")

    # Recommendation
    st.markdown("## AI Recommendation")

    if d["final_score"] >= 80:
        st.success("🔥 Strong Hire Candidate")
    elif d["final_score"] >= 60:
        st.warning("⚠️ Moderate Candidate")
    else:
        st.error("❌ Not Recommended")

    # Chart
    df = pd.DataFrame({
        "Category": ["Skills", "Experience", "Keyword"],
        "Score": [
            d["skills_score"],
            d["experience_score"],
            d["keyword_score"]
        ]
    })

    fig = px.bar(df, x="Category", y="Score", text="Score")
    st.plotly_chart(fig, use_container_width=True)

    # Download Report
    st.download_button(
        label="Download Report",
        data=str(d),
        file_name="resume_report.txt"
    )
