import pytesseract
from PIL import Image
import shutil

# auto detect tesseract (works on Render + local)
pytesseract.pytesseract.tesseract_cmd = shutil.which("tesseract") or "tesseract"


def extract_image_text(path):
    try:
        img = Image.open(path)
        img = img.convert("L")
        return pytesseract.image_to_string(img)
    except Exception as e:
        return f"OCR Error: {str(e)}"