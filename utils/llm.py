import streamlit as st
from groq import Groq

# ---------------- CLIENT ----------------
client = Groq(api_key=st.secrets["GROQ_API_KEY"])


# ---------------- TEXT LLM ----------------
def call_llm(prompt, max_tokens=300):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens
    )
    return response.choices[0].message.content.strip()


# ---------------- IMAGE VISION ----------------
def call_vision_llm(base64_image):
    response = client.chat.completions.create(
        model="llama-3.2-11b-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Extract all meaningful information from this image. Provide summary and key points."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        },
                    },
                ],
            }
        ],
        max_tokens=500,
    )

    return response.choices[0].message.content.strip()