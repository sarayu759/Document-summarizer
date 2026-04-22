import pytesseract
from PIL import Image

# 🔴 SET PATH (important)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Load image
img = Image.open("test.png")

# Convert to grayscale (improves accuracy)
img = img.convert("L")

# Extract text
text = pytesseract.image_to_string(img)

print("OCR RESULT:")
print(text)