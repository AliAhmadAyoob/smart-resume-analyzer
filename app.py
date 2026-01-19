from resume_parser import parsed_resume
from matcher import match_skills, match_experience, match_projects, contact_score
from skill_extractor import extract_skills, extract_experience
import streamlit as st

st.set_page_config(page_title="Smart Resume Analyzer", layout="wide")
st.title("Smart Resume Analyzer 📝")

uploaded_file = st.file_uploader("Upload your Resume (PDF or TXT)", type=["pdf", "txt"])

if uploaded_file:
    parsed = parsed_resume(uploaded_file)
    st.success("Resume Parsed Successfully!")
    st.write("Candidate Name:", parsed.get("name", "N/A"))

    jb_desc = st.text_area("Paste the Job Description here")

    if jb_desc:
        jb_exp = extract_experience(jb_desc)
        jb_skill = extract_skills(jb_desc)

        # ✅ convert resume experience list → text
        resume_exp_text = " ".join(parsed.get("experience", []))
        res_exp = extract_experience(resume_exp_text)

        scores = {}
        feedback = []

        s, f = match_skills(jb_skill, parsed.get("skills", []))
        scores["skills_score"] = s
        feedback.extend(f)

        s, f = match_experience(jb_exp, res_exp)
        scores["experience_score"] = s
        feedback.extend(f)

        s, f = match_projects(jb_skill, parsed.get("projects", []))
        scores["project_score"] = s
        feedback.extend(f)

        s, f = contact_score(parsed)
        scores["contact_score"] = s
        feedback.extend(f)

        overall_score = (
            0.5 * scores.get("skills_score", 0) +
            0.3 * scores.get("experience_score", 0) +
            0.15 * scores.get("project_score", 0) +
            0.05 * scores.get("contact_score", 0)
        )

        st.subheader("Resume Analysis Results")
        st.metric("Overall Score", f"{overall_score:.2f}%")

        st.write("### Score Breakdown")
        st.write(scores)

        st.write("### Feedback / Suggestions")
        for f in feedback:
            st.write("•", f)
