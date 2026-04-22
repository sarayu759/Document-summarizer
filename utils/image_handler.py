import pytesseract
from PIL import Image

# IMPORTANT
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_image_text(path):
    try:
        img = Image.open(path)

        # improve OCR
        img = img.convert("L")
        img = img.resize((img.width * 2, img.height * 2))

        text = pytesseract.image_to_string(img, config='--psm 6')

        return text

    except Exception as e:
        return f"OCR Error: {str(e)}"