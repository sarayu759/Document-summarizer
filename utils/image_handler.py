def extract_image_text(path):
    try:
        from PIL import Image
        import pytesseract

        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

        img = Image.open(path)
        text = pytesseract.image_to_string(img)

        print("OCR TEXT:", text)  # debug

        return text.strip()

    except Exception as e:
        print("OCR ERROR:", e)
        return ""