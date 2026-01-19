import streamlit as st

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

        # ---------------- RESULTS ----------------
        st.subheader("Resume Analysis Results")
        st.metric("Overall Match Score", f"{overall_score:.2f}%")

        st.write("### Score Breakdown")
        st.write(scores)

        st.write("### Feedback & Suggestions")
        if feedback:
            for fb in feedback:
                st.write("•", fb)
        else:
            st.success("Great job! Your resume matches the job description well.")
