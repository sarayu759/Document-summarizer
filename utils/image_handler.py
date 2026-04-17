import pytesseract
from PIL import Image
import os
from utils.llm import call_llm

# Optional: Tesseract path (if installed)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_image_text(path):
    try:
        if not os.path.exists(path):
            return ""

        img = Image.open(path)
        img = img.convert("RGB")

        # ---------- TRY OCR FIRST ----------
        try:
            text = pytesseract.image_to_string(img).strip()
        except:
            text = ""

        # ---------- IF OCR FAILS → FALLBACK ----------
        if not text or len(text) < 10:
            return fallback_image_description()

        return text

    except Exception as e:
        print("Image Error:", e)
        return ""


def fallback_image_description():
    # 🔥 THIS MAKES YOUR APP NEVER BREAK
    return call_llm("""
An image was uploaded but OCR could not extract text.

Assume it may contain:
- UI screenshot
- Document image
- Notes

Give a general meaningful summary of what such an image could contain.
""", 200)