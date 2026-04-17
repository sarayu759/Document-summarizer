import streamlit as st
from groq import Groq
from openai import OpenAI

# -------- CLIENTS --------
groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
openai_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


# -------- TEXT (GROQ) --------
def call_llm(prompt, max_tokens=300):
    response = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens
    )
    return response.choices[0].message.content.strip()


# -------- IMAGE (OPENAI) --------
def call_image_llm(base64_image):
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Extract all text and summarize this image clearly."},
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