import pdfplumber as pd
import docx

def text_extracter(file):
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
