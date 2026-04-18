from PIL import Image
import pytesseract
import shutil

def extract_image_text(path):
    # 🔍 Check if tesseract exists
    tesseract_path = shutil.which("tesseract")

    if not tesseract_path:
        return "⚠️ OCR not available (Tesseract not installed in environment)"

    # ✅ Set path
    pytesseract.pytesseract.tesseract_cmd = tesseract_path

    # 🔍 Process image
    img = Image.open(path)
    text = pytesseract.image_to_string(img)

    if not text.strip():
        return "⚠️ No readable text found in image"

    return text