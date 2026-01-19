from resume_parser import parsed_resume
from matcher import match_skills_exp,match_exp,contact_score
from skill_extractor import extract_skills,extract_experience
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

    exp = extract_experience(parsed['experience'])
    
    match_skills_exp(jb_skill,parsed['skills'])
    match_exp(jb_exp,exp)
    match_projects(jb_skills,parsed['projects'])
    score = contact_score(parsed)
    
    overall_score = (
        0.5 * score.get('skills_score',0) +
        0.3 * score.get('experience_score',0) +
        0.15 * score.get('project_score',0) +
        0.05 * score.get('contact_score',0)
    )
    st.subheader("Resume Analysis Results")
    st.metric("Overall Score", f"{overall_score:.2f}%")

    st.write("### Score Breakdown")
    st.write(score)

    st.write("### Feedback / Suggestions")
    for f in feedback:
        st.write("-", f)
