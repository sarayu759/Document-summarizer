from PIL import Image
import pytesseract
import os

# 🔥 FORCE PATH (RENDER)
TESSERACT_PATH = "/usr/bin/tesseract"

# 🔥 HARD FAIL IF NOT PRESENT
if not os.path.exists(TESSERACT_PATH):
    raise RuntimeError("❌ Tesseract not installed at /usr/bin/tesseract")

# 🔥 SET PATH
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


def extract_image_text(path):
    img = Image.open(path)
    text = pytesseract.image_to_string(img)

    if not text.strip():
        return "⚠️ No readable text found in image"

    return text