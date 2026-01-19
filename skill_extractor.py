skills_db = {
    "Python": ["python", "py"],
    "Java": ["java"],
    "C++": ["c++", "cpp"],
    "SQL": ["sql", "structured query language","mysql"],
    "JavaScript": ["javascript", "js"],
    "React": ["react", "react.js", "reactjs"],
    "Node.js": ["node.js", "nodejs"],
    "Docker": ["docker", "docker container"],
    "AWS": ["aws", "amazon web services"],
    "TensorFlow": ["tensorflow", "tf"],
    "Machine Learning": ["machine learning", "ml"],
    "Excel": ["excel", "ms excel", "microsoft excel"],
    "Git": ["git", "github", "gitlab"],
    "Deep Learning": ["dl"],
    "NLP": ["natural language processing"],
    "Kubernetes": ["k8s"],
}

def extract_skills(resume_text):
    found_skills = []

    for skill,variations in skills_db.items():
        for var in variations:
            if var in resume_text.lower():
                found_skills.append(skill)
                break
    return list(set(found_skills))

def extract_experience(jd_text):
    jd_text = jd_text.lower()
    patterns = [
        r'(\d+)\s*-\s*(\d+)\s*years',  
        r'minimum\s*(\d+)\s*years',   
        r'at least\s*(\d+)\s*years',   
        r'(\d+)\s*years'               
    ]
    
    for pattern in patterns:
        match = re.search(pattern, jd_text)
        if match:
            if len(match.groups()) == 2:
                return int(match.group(1)) * 12  # convert to months
            else:
                return int(match.group(1)) * 12  # convert to months
    return 0  