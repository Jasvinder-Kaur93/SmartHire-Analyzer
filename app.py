import streamlit as st
import pandas as pd
import plotly.express as px

from backend.parser import (
    extract_text_from_pdf,
    extract_text_from_docx,
    extract_contact_info,
    extract_experience
)

from backend.skills import extract_skills, TECH_SKILLS
from backend.matcher import compute_match_score
from backend.database import save_candidate


# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(
    page_title="Smart Hire Analyzer",
    page_icon="📄",
    layout="wide"
)


# ==============================
# LOAD CSS
# ==============================
def load_css():
    with open("frontend/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()


# ==============================
# SESSION STATE INIT
# ==============================
if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False


# ==============================
# RESET BUTTON
# ==============================
if st.button("🔄 Reset Analysis"):
    st.session_state.analysis_done = False
    st.rerun()


# ==============================
# HEADER
# ==============================
st.markdown("""
<h1>Smart Hire Analyzer</h1>
<p style='text-align:center;color:#94a3b8;font-size:16px;'>
Offline AI-Powered ATS Resume Screening System
</p>
""", unsafe_allow_html=True)

st.markdown("---")


# ==============================
# INPUT SECTION
# ==============================
st.markdown("## 📥 Upload Resume & Job Description")

col1, col2 = st.columns([1, 1.2])

with col1:
    uploaded_file = st.file_uploader(
        "📄 Upload Resume",
        type=["pdf", "docx"]
    )

with col2:
    job_description = st.text_area(
        "🧠 Paste Job Description"
    )


# ==============================
# ANALYZE BUTTON
# ==============================
analyze = st.button("🚀 Analyze Resume")


# ==============================
# ANALYSIS PIPELINE
# ==============================
if analyze:

    if not uploaded_file:
        st.warning("Please upload a resume")
        st.stop()

    if not job_description.strip():
        st.warning("Please enter job description")
        st.stop()

    with st.spinner("Extracting resume content..."):

        if uploaded_file.type == "application/pdf":
            text = extract_text_from_pdf(uploaded_file)
        else:
            text = extract_text_from_docx(uploaded_file)

    with st.spinner("Analyzing profile & skills..."):

        info = extract_contact_info(text)
        skills = extract_skills(text)
        experience = extract_experience(text)

    with st.spinner("Calculating ATS match score..."):

        keyword_score = compute_match_score(text, job_description)


    # ==============================
    # SCORE ENGINE
    # ==============================
    skills_score = min(len(skills) * 12, 100)

    try:
        experience_score = min(int(experience) * 10, 100)
    except:
        experience_score = 0

    final_score = round(
        (0.4 * skills_score) +
        (0.2 * experience_score) +
        (0.4 * keyword_score),
        2
    )

    # ==============================
    # SAVE DATA
    # ==============================
    save_candidate({
        "name": info["name"],
        "email": info["email"],
        "phone": info["phone"],
        "skills": ", ".join(skills),
        "experience": experience,
        "score": final_score
    })

    # ==============================
    # SESSION STATE
    # ==============================
    st.session_state.info = info
    st.session_state.skills = skills
    st.session_state.experience = experience
    st.session_state.final_score = final_score
    st.session_state.skills_score = skills_score
    st.session_state.experience_score = experience_score
    st.session_state.keyword_score = keyword_score
    st.session_state.analysis_done = True


# ==============================
# RESULTS SECTION
# ==============================
if st.session_state.analysis_done:

    info = st.session_state.info
    skills = st.session_state.skills
    experience = st.session_state.experience
    final_score = st.session_state.final_score
    skills_score = st.session_state.skills_score
    experience_score = st.session_state.experience_score
    keyword_score = st.session_state.keyword_score


    # ==============================
    # REPORT HEADER
    # ==============================
    st.markdown("## 📄 Candidate Evaluation Report")

    st.markdown(f"""
    <div style="
        background: rgba(255,255,255,0.05);
        padding: 18px;
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.1);
    ">
        <h3>Summary</h3>
        <div><b>Name:</b> {info['name']}</div>
        <div><b>Experience:</b> {experience} years</div>
        <div><b>Skills Found:</b> {len(skills)}</div>
        <div><b>Final ATS Score:</b> {final_score}%</div>
    </div>
    """, unsafe_allow_html=True)


    st.markdown("---")


    # ==============================
    # ATS SCORE BREAKDOWN CARDS
    # ==============================
    st.markdown("## 🎯 ATS Score Breakdown")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(f"""
        <div style="
            background: rgba(59,130,246,0.12);
            padding: 20px;
            border-radius: 16px;
            text-align: center;
        ">
            <h3 style="color:#3b82f6;">Skills</h3>
            <h2>{skills_score}/100</h2>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div style="
            background: rgba(34,197,94,0.12);
            padding: 20px;
            border-radius: 16px;
            text-align: center;
        ">
            <h3 style="color:#22c55e;">Experience</h3>
            <h2>{experience_score}/100</h2>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div style="
            background: rgba(168,85,247,0.12);
            padding: 20px;
            border-radius: 16px;
            text-align: center;
        ">
            <h3 style="color:#a855f7;">Keyword</h3>
            <h2>{keyword_score:.1f}/100</h2>
        </div>
        """, unsafe_allow_html=True)


    st.markdown("---")


    # ==============================
    # FINAL SCORE CARD
    # ==============================
    color = "#22c55e" if final_score >= 75 else "#f59e0b" if final_score >= 50 else "#ef4444"

    st.markdown("## 🏆 Final ATS Score")

    st.markdown(f"""
    <div style="
        background: rgba(255,255,255,0.05);
        padding: 30px;
        border-radius: 18px;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.1);
    ">
        <h1 style="color:{color}; font-size:55px;">
            {final_score}%
        </h1>
        <p style="color:#94a3b8;">Overall ATS Compatibility Score</p>
    </div>
    """, unsafe_allow_html=True)


    st.markdown("---")


    # ==============================
    # AI RECOMMENDATION (FIXED)
    # ==============================
    st.markdown("## 🤖 AI Recommendation")

    if final_score >= 85:
        st.success("Strong Hire — Highly recommended for interview round")

    elif final_score >= 70:
        st.info("Good Candidate — Recommended for HR screening")

    elif final_score >= 50:
        st.warning("Moderate Fit — Needs review before decision")

    else:
        st.error("Low Match — Not aligned with job requirements")


    st.caption(
        "AI Insight: Recommendation is based on skills match, experience level, and keyword similarity with job description."
    )


    st.markdown("---")


    # ==============================
    # SKILL GAPS
    # ==============================
    st.markdown("## 🎯 Skill Gap Analysis")

    required_skills = ["python", "sql", "machine learning", "communication"]

    missing = [s for s in required_skills if s not in [x.lower() for x in skills]]

    if missing:
        for m in missing:
            st.markdown(f"• Improve: {m}")
    else:
        st.success("No major skill gaps detected")


    st.markdown("---")


    # ==============================
    # SKILL GRAPH
    # ==============================
    st.markdown("## 📊 Skill Distribution")

    categories = {
        "Programming": 0,
        "Web": 0,
        "Database": 0,
        "Cloud": 0,
        "AI": 0
    }

    for skill in skills:
        for cat, skill_list in TECH_SKILLS.items():
            if skill.lower() in skill_list:
                categories[cat] += 1

    df = pd.DataFrame({
        "Category": list(categories.keys()),
        "Skills": list(categories.values())
    })

    fig = px.bar(
        df,
        x="Category",
        y="Skills",
        text="Skills",
        color="Category",
        title="Skill Distribution"
    )

    fig.update_layout(
        paper_bgcolor="#0b1220",
        plot_bgcolor="#0b1220",
        font_color="white"
    )

    st.plotly_chart(fig, use_container_width=True)


    st.markdown("---")


    # ==============================
    # CANDIDATE DETAILS
    # ==============================
    st.markdown("## 👤 Candidate Details")

    st.markdown(f"""
    <div style="
        background: rgba(255,255,255,0.04);
        padding: 16px;
        border-radius: 14px;
        color: #cbd5e1;
        font-size: 14px;
        line-height: 1.8;
    ">
        <div><b>Name:</b> {info['name']}</div>
        <div><b>Email:</b> {info['email']}</div>
        <div><b>Phone:</b> {info['phone']}</div>
    </div>
    """, unsafe_allow_html=True)


# ==============================
# FOOTER
# ==============================
st.markdown("---")
st.markdown(
    "<p style='text-align:center;color:#64748b;'>Smart Hire Analyzer © 2026</p>",
    unsafe_allow_html=True
)