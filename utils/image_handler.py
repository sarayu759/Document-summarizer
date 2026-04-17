import pytesseract
from PIL import Image
import os

# 🔥 SET TESSERACT PATH (VERY IMPORTANT)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_image_text(path):
    try:
        # ✅ Check file exists
        if not os.path.exists(path):
            return ""

        # ✅ Open image
        img = Image.open(path)

        # ✅ Convert to RGB (fix some PNG issues)
        img = img.convert("RGB")

        # ✅ OCR extraction
        text = pytesseract.image_to_string(img)

        # ✅ Clean text
        text = text.strip()

        # ❌ If no text found
        if not text:
            return ""

        return text

    except Exception as e:
        print("Image OCR Error:", e)
        return ""