def match_skills(jb_skills, resume_skills):
    jb = set(skill.lower() for skill in jb_skills)
    rs = set(skill.lower() for skill in resume_skills)

    matched = jb.intersection(rs)
    missing = jb - rs

    score = (len(matched) / len(jb)) * 100 if jb else 0

    feedback = []
    if missing:
        feedback.append(f"Add missing skills: {', '.join(missing)}")

    return score, feedback
def match_experience(jb_exp, resume_exp):
    feedback = []

    try:
        jb_exp = int(jb_exp)
        resume_exp = int(resume_exp)
    except:
        return 0, ["Experience not clearly mentioned"]

    if resume_exp >= jb_exp:
        return 100, []
    else:
        score = (resume_exp / jb_exp) * 100
        feedback.append(f"Gain at least {jb_exp - resume_exp} more years of experience")
        return score, feedback
def match_projects(jd_keywords, projects):
    feedback = []
    matched = 0
    required = 3

    projects_text = " ".join(projects).lower()

    for kw in jd_keywords:
        if kw.lower() in projects_text:
            matched += 1

    score = min((matched / required) * 100, 100)

    if matched < required:
        feedback.append("Add more relevant projects related to the job description")

    return score, feedback
def contact_score(parsed):
    feedback = []
    score = 10 if parsed.get("contact", {}).get("email") and parsed.get("contact", {}).get("phone") else 0

    if score == 0:
        feedback.append("Include both email and phone number")

    return score, feedback
