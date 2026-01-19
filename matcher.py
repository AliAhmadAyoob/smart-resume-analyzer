score = {}
feedback = []
def match_skills_exp(jb_skills,skills):
    matched_skills = [skill for skill in skills if skill in jb_skills]
    skill_score = (len(matched_skills)/len(jb_desc)) *100 
    score['skills_score']=skill_score
    missing_skills = [skill for skill in jd_skills if skill not in parsed["skills"]]
    if missing_skills:
        feedback.append(f"Add missing skills: {missing_skills}")

def match_exp(jb_exp,exp):
    if exp is None or exp == '0' or exp == 0:
        score['expreience_score'] = 0 
    elif exp >= jb_exp:
        score['expreience_score'] = 100
    else:
        score['expreience_score'] = (exp / jb_exp) * 100
        feedback.append(f"Gain more experience: {required_exp_months//12} years required")

def match_projects(jb_desc , projects):
    matched = 0
    num_required_projects = 3
    for project in projects.lower():
        for keyword in jd_desc:
            if keyword.lower() in project:
                matched +=1
                break
    project_score = min((matched_projects / num_required_projects) * 100, 100)
    score['project_score'] = project_score
    if matched_projects < num_required_projects:
        feedback.append(f"Add more projects related to: {', '.join(jd_project_keywords)}")

def contact_score(parsed):
    contact_score = 10 if parsed["contact"]["email"] and parsed["contact"]["phone"] else 0
    score['contact_score'] = contact_score
    if not parsed["contact"]["email"] or not parsed["contact"]["phone"]:
        feedback.append(f"Include email and phone number")

    return score
