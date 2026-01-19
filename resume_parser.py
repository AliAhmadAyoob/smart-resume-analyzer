import pdfplumber as pd
import docx
import re
from skill_extractor import extract_skills,skills_db
from utils import clean_text
def text_extractor(file):
    text = ""
    if file.endswith('.pdf'):
        with pd.open(file) as pdf:
            for page in pdf.pages:
                if page.extract_text():
                    text += page.extract_text() +'\n'
    elif file.endswith('.docx'):
        doc = docx.Document(file)
        for para in doc.paragraphs:
            text += para.text+'\n'
    else:
        raise ValueError("Unsopported File Format")
    return text

def extract_contact(text):
    email = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    phone = re.findall(r"\+?\d[\d\s\-]{7,}\d", text)
    return {
        "email": email[0] if email else None,
        "phone": phone[0] if phone else None
    }
    
def extract_name(text):
    lines = text.split("\n")
    first_line = lines[0].strip()

    if not any(char.isdigit() for char in first_line) and len(first_line.split()) <= 4:
        return first_line
    return None

def extract_education(text):
    edu_keywords = ["bachelor", "master", "bsc", "msc", "bs", "ms", "university", "college", "gpa", "phd"]
    education = []

    for line in text.split('\n'):
        if any(k in line.lower() for k in edu_keywords):
            education.append(line.strip())
            print(line)
    return education

def extract_expereince(text):
    exp_keywords = ["worked","built", "managed", "led", "experience"]
    experience = []
    for line in text.split('\n'):
        if any(k in line.lower() for k in exp_keywords):
            experience.append(line.strip())
    return experience

def extract_certifications(text):
    cert_keys = ["certified", "certification", "course", "training", "diploma", "certificate"]
    certs = []
    for line in text.split('\n'):
     if any(k in line.lower() for k in cert_keys):
         certs.append(line)
    return certs

def extract_projects(text):
    proj_keys = ["project", "developed", "built", "implemented", "application", "system"]
    projects = []

    for line in text.split("\n"):
        if any(k in line.lower() for k in proj_keys):
            projects.append(line.strip())

    return projects

def parse_resume(file,skills_db=skills_db):
    text = text_extractor(file)
    cleaned_text = clean_text(text)
    parsed = {
        "name":extract_name(text),
        "contact": extract_contact(text),
        "education":extract_education(text),
        "skills": extract_skills(cleaned_text),
        "experience":extract_expereince(text),
        "certifications":extract_certifications(text),
        "projects":extract_projects(text)
    }
    
    return parsed
