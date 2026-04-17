import base64
from utils.llm import client


def extract_image_text(path):
    try:
        with open(path, "rb") as f:
            image_data = base64.b64encode(f.read()).decode()

        response = client.chat.completions.create(
            model="llama-3.2-11b-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Extract all meaningful information from this image. Give a clear summary and key points."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{image_data}"
                            },
                        },
                    ],
                }
            ],
            max_tokens=500,
        )

        return response.choices[0].message.content

    except Exception as e:
        print("Vision Error:", e)
        return ""