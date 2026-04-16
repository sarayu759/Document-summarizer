import re

def clean_text(text):
    if not text:
        return ""
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'(.)\1{4,}', '', text)
    return text.strip()