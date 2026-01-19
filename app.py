import streamlit as st
import matplotlib.pyplot as plt

from resume_parser import parsed_resume
from skill_extractor import extract_skills, extract_experience
from matcher import (
    match_skills,
    match_experience,
    match_projects,
    contact_score
)


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Smart Resume Analyzer",
    layout="wide"
)

st.title("Smart Resume Analyzer 📝")
st.write("Analyze how well a resume matches a job description.")

# ---------------- RESUME UPLOAD ----------------
uploaded_file = st.file_uploader(
    "Upload your Resume (PDF or TXT)",
    type=["pdf", "txt"]
)

if uploaded_file:
    parsed = parsed_resume(uploaded_file)

    st.success("Resume parsed successfully!")

    st.subheader("Candidate Information")
    st.write("**Name:**", parsed.get("name", "N/A"))

    # ---------------- JOB DESCRIPTION ----------------
    jb_desc = st.text_area(
        "Paste the Job Description here",
        height=250
    )

    if jb_desc:
        # -------- Extract JD info --------
        jb_skills = extract_skills(jb_desc)
        jb_exp = extract_experience(jb_desc)

        # -------- Extract Resume info --------
        resume_skills = parsed.get("skills", [])
        resume_projects = parsed.get("projects", [])

        # Convert experience list → string → number
        resume_exp_text = " ".join(parsed.get("experience", []))
        resume_exp = extract_experience(resume_exp_text)

        scores = {}
        feedback = []

        # -------- Skill Matching --------
        s, f = match_skills(jb_skills, resume_skills)
        scores["skills_score"] = s
        feedback.extend(f)

        # -------- Experience Matching --------
        s, f = match_experience(jb_exp, resume_exp)
        scores["experience_score"] = s
        feedback.extend(f)

        # -------- Project Matching --------
        s, f = match_projects(jb_skills, resume_projects)
        scores["project_score"] = s
        feedback.extend(f)

        # -------- Contact Info --------
        s, f = contact_score(parsed)
        scores["contact_score"] = s
        feedback.extend(f)

        # -------- Overall Score --------
        overall_score = (
            0.5 * scores.get("skills_score", 0) +
            0.3 * scores.get("experience_score", 0) +
            0.15 * scores.get("project_score", 0) +
            0.05 * scores.get("contact_score", 0)
        )
        st.markdown(
        f"""
        <div style="text-align:center; padding:20px; border-radius:15px; 
                    background:#f5f7fa; margin-bottom:20px;">
            <h2>Overall ATS Match</h2>
            <h1 style="color:#4CAF50;">{overall_score:.2f}%</h1>
        </div>
        """,
        unsafe_allow_html=True
    )
        labels = ["Skills", "Experience", "Projects", "Contact"]
        values = [
            scores["skills_score"],
            scores["experience_score"],
            scores["project_score"],
            scores["contact_score"]
        ]
        
        fig, ax = plt.subplots()
        ax.pie(
            values,
            labels=labels,
            autopct="%1.1f%%",
            startangle=90,
            wedgeprops=dict(width=0.35)
        )
        ax.set_title("ATS Scoring Breakdown")
        
        st.pyplot(fig)
        
        # ----- Score Cards -----
        col1, col2, col3, col4 = st.columns(4)
        
        col1.metric("Skills", f"{scores['skills_score']:.1f}%")
        col2.metric("Experience", f"{scores['experience_score']:.1f}%")
        col3.metric("Projects", f"{scores['project_score']:.1f}%")
        col4.metric("Contact", f"{scores['contact_score']:.1f}/10")
        # ---------------- RESULTS ----------------
        st.subheader("Feedback & Suggestions")
        for fb in feedback:
            st.write("•", fb)


        # st.write("### Score Breakdown")
        # st.write(scores)

        # st.write("### Feedback & Suggestions")
        # if feedback:
        #     for fb in feedback:
        #         st.write("•", fb)
        else:
            st.success("Great job! Your resume matches the job description well.")
