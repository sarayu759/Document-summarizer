from PIL import Image
import pytesseract

def extract_image_text(path):
    try:
        img = Image.open(path)
        text = pytesseract.image_to_string(img)

        if text.strip():
            return text

        return "⚠️ No readable text found in image"

    except Exception as e:
        return f"❌ OCR Error: {str(e)}"