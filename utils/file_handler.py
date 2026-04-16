from utils.pdf_handler import extract_pdf_text
from utils.image_handler import extract_image_text
from utils.csv_handler import extract_csv_text
from utils.cleaner import clean_text


def extract_text(path, file_type):
    if file_type == "pdf":
        text = extract_pdf_text(path)

    elif file_type == "image":
        text = extract_image_text(path)

    elif file_type == "csv":
        text = extract_csv_text(path)

    else:
        text = ""

    return clean_text(text)