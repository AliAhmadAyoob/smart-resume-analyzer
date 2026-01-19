def match_skills(jb_skills, resume_skills):
    jb = set(s.lower() for s in jb_skills)
    rs = set(s.lower() for s in resume_skills)

    matched = jb & rs
    missing = jb - rs

    score = (len(matched) / len(jb)) * 100 if jb else 0

    feedback = []

    if matched:
        feedback.append(f"✓ You've already highlighted: {', '.join(matched)}")

    if missing:
        feedback.append(f"⚠ Missing important keywords: {', '.join(missing)}")
        feedback.append("Tip: Add these in your Skills section and relevant projects to improve ATS matching.")

    return score, feedback


def match_experience(jb_exp, resume_exp):
    feedback = []

    try:
        jb_exp = int(jb_exp)
        resume_exp = int(resume_exp)
    except:
        return 0, ["Specify work experience clearly in years (e.g., '2 years as Data Analyst')"]

    if resume_exp >= jb_exp:
        return 100, ["Great! Your experience meets the job requirement."]

    gap = jb_exp - resume_exp
    score = (resume_exp / jb_exp) * 100

    feedback.append(f"⚠ Experience gap: {gap} year(s)")
    feedback.append("Tip: Compensate by showcasing high-impact projects, internships, or certifications.")

    return score, feedback


def match_projects(jd_keywords, projects):
    feedback = []
    matched = 0
    required = 3  # adjustable benchmark

    project_text = " ".join(projects).lower()

    for kw in jd_keywords:
        if kw.lower() in project_text:
            matched += 1

    score = min((matched / required) * 100, 100)

    if matched >= required:
        feedback.append("✓ Your projects align well with the job role.")
    else:
        missing = required - matched
        feedback.append(f"⚠ Add {missing} more relevant project(s) aligned with the job.")
        feedback.append("Tip: Include tools, responsibilities & outcomes (e.g., 'Improved accuracy by 18%').")

    return score, feedback


def contact_score(parsed):
    feedback = []
    contact = parsed.get("contact", {})

    score = 0

    if contact.get("email"):
        score += 3
    else:
        feedback.append("⚠ Add a professional email (e.g., firstname.lastname@gmail.com)")

    if contact.get("phone"):
        score += 3
    else:
        feedback.append("⚠ Add a phone number with country code")

    if contact.get("linkedin"):
        score += 2
    else:
        feedback.append("Tip: Include LinkedIn to improve credibility")

    if contact.get("portfolio") or contact.get("github"):
        score += 2
    else:
        feedback.append("Tip: Add portfolio or GitHub link especially for tech roles")

    return score, feedback


def compute_overall_score(skill_s, exp_s, proj_s, contact_s):
    # Weighted score - feels more realistic
    return round((skill_s * 0.4) + (exp_s * 0.3) + (proj_s * 0.2) + (contact_s * 0.1), 2)
