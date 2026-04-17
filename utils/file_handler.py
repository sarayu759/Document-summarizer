from utils.pdf_handler import extract_pdf_text
from utils.csv_handler import extract_csv_text

def extract_text(path, file_type):
    if file_type == "pdf":
        return extract_pdf_text(path)

    elif file_type == "csv":
        return extract_csv_text(path)

    return ""