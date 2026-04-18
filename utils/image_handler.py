from PIL import Image
import base64
import io

from utils.llm import call_image_llm


def extract_image_text(path):
    try:
        # ✅ Load image safely
        img = Image.open(path).convert("RGB")

        # ✅ Resize (prevents large request errors)
        img = img.resize((512, 512))

        # ✅ Convert to base64
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        base64_image = base64.b64encode(buffer.getvalue()).decode()

        # ✅ Send to AI model
        result = call_image_llm(base64_image)

        # ✅ Clean fallback
        if not result or "error" in result.lower():
            return "⚠️ Could not extract meaningful content from image"

        return result

    except Exception as e:
        return f"❌ Image processing failed: {str(e)}"