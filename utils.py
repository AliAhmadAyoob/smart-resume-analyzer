import re
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
words_to_retain = {"c", "r", "ai", "ml", "sql", "js", "html", "css", "c++", "c#", "django", "react"}
unwanted= {"email", "website", "skills", "phone", "linkedin"}
stop_words = set(stopwords.words('english'))

def clean_text(text):
    text = text.lower()
    text = re.sub(r'\S+@\S+','',text)
    text = re.sub(r'http\S+|www.\S+','',text)
    text = re.sub(r'[^a-z0-9\s+#]',' ',text)
    words = text.split()

    cleaned_text = ' '.join([w for w in words if (w not in stop_words or w in words_to_retain) and w not in unwanted])
    cleaned_text = re.sub(r'\s+',' ',cleaned_text).strip()

    return cleaned_text    