import pytesseract
from PIL import Image
import shutil

pytesseract.pytesseract.tesseract_cmd = shutil.which("tesseract") or "tesseract"

def extract_image_text(path):
    try:
        img = Image.open(path)

        # 🔥 resize for faster OCR
        img = img.resize((800, 800))

        # convert to grayscale
        img = img.convert("L")

        return pytesseract.image_to_string(img)

    except Exception as e:
        return f"OCR Error: {str(e)}"