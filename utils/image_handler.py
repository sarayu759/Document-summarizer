import base64
from utils.llm import call_vision_llm


def extract_image_text(path):
    try:
        # read image
        with open(path, "rb") as f:
            image_bytes = f.read()

        # convert to base64
        base64_image = base64.b64encode(image_bytes).decode("utf-8")

        # call vision model
        result = call_vision_llm(base64_image)

        return result

    except Exception as e:
        print("Image processing error:", e)
        return ""