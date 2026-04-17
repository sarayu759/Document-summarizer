from pypdf import PdfReader


def extract_pdf_text(path):
    reader = PdfReader(path)
    text = ""

    for page in reader.pages:
        t = page.extract_text()
        if t:
            text += t + "\n"

    return text