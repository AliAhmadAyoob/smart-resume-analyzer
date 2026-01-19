
import streamlit as st
import plotly.graph_objects as go

# --- KEEP YOUR ACTUAL IMPORTS HERE ---
from resume_parser import parsed_resume
from skill_extractor import extract_skills, extract_experience
from matcher import match_skills, match_experience, match_projects, contact_score

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Smart Resume Analyzer",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- ENHANCED CUSTOM CSS ----------------
st.markdown("""
    <style>
    /* Main background and font */
    .stApp {
        background-color: #fcfcfc;
    }
    
    /* Overall Score Card Style */
    .overall-score-container {
        background: #ffffff;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #e6e9ef;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        text-align: center;
        margin-bottom: 20px;
    }

    /* Metric Card Styling */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e6e9ef;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        font-weight: 600;
    }

     /* Enhanced fix for truncation and alignment */
    [data-testid="stMetricValue"] {
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        color: #31333F;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.85rem !important;
        color: #555e6d;
}
    </style>
    """, unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/942/942799.png", width=80)

    st.title("Navigation")
    uploaded_file = st.file_uploader(
        "Upload your Resume (PDF or TXT)",
        type=["pdf", "txt"]
    )
    st.divider()
    st.info("The analyzer compares your resume against the job description to provide an ATS score.")

# ---------------- MAIN CONTENT ----------------
st.title("Smart Resume Analyzer 📝")
st.caption("Optimize your resume for Applicant Tracking Systems (ATS)")
st.markdown("---")

if uploaded_file:
    # --- YOUR ACTUAL PARSING LOGIC HERE ---
    parsed = parsed_resume(uploaded_file)
    
    st.success(f"✅ Loaded: **{parsed.get('name', 'Candidate')}**")

    col_input, col_viz = st.columns([1, 1], gap="large")

    with col_input:
        st.subheader("🎯 Job Description")
        jb_desc = st.text_area("Paste the requirements here", height=280, placeholder="Enter skills, qualifications, and responsibilities...")
    if jb_desc:
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
        with col_viz:
            st.subheader("📊 Match Analysis")
            
            # --- BEAUTIFIED PLOTLY DONUT ---
            fig = go.Figure(data=[go.Pie(
                labels=["Skills", "Experience", "Projects", "Contact"],
                values=[scores["skills_score"], scores["experience_score"], scores["project_score"], scores["contact_score"]],
                hole=.65,
                marker=dict(colors=['#00D1B2', '#3273DC', '#FFDD57', '#F03D5F']),
                hoverinfo='label+percent',
                textinfo='none' # Keep it clean, center text handles the rest
            )])
            
            fig.update_layout(
                annotations=[dict(text=f'<b>{overall_score}%</b>', x=0.5, y=0.5, font_size=28, showarrow=False, font_color="#363636")],
                margin=dict(t=10, b=10, l=10, r=10),
                height=300,
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
            )
            st.plotly_chart(fig, use_container_width=True)
    
            # ---------------- SCORE METRICS ----------------
            st.markdown("### Breakdown by Category")
            m1, m2, m3, m4 = st.columns(4)
            
            # We calculate the "delta" (difference from 100) to show how much room for improvement exists
            m1.metric("Skills", f"{scores['skills_score']:.2f}%")
            m2.metric("Experience", f"{scores['experience_score']:.2f}%")
            m3.metric("Projects", f"{scores['project_score']:.2f}%")
            m4.metric("Contact", f"{scores['contact_score']:.2f}/10")

            # ---------------- FEEDBACK TABS ----------------
            st.markdown("<br>", unsafe_allow_html=True)
            tab1, tab2 = st.tabs(["💡 Improvement Tips", "📄 Data Preview"])
            
            with tab1:
                for fb in feedback:
                    st.write(f"✅ {fb}")
                if overall_score > 80:
                    st.balloons()
    
            with tab2:
                st.json(parsed)

else:
    st.warning("Please upload a resume in the sidebar to begin.")
    st.image("svg-repo.svg", width=350)



