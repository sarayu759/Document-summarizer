import streamlit as st
from groq import Groq
from openai import OpenAI
import time

# -------- SAFE CLIENT INIT --------
def get_key(name):
    if name in st.secrets:
        return st.secrets[name]
    else:
        st.error(f"❌ Missing {name} in secrets")
        st.stop()

groq_client = Groq(api_key=get_key("GROQ_API_KEY"))
openai_client = OpenAI(api_key=get_key("OPENAI_API_KEY"))


# -------- TEXT (GROQ) --------
def call_llm(prompt, max_tokens=300):
    try:
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt[:4000]}],
            max_tokens=max_tokens
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Groq Error: {str(e)}"


# -------- IMAGE (OPENAI SAFE + RETRY) --------
def call_image_llm(base64_image):
    for _ in range(3):
        try:
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Summarize this image clearly."},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{base64_image}"
                                },
                            },
                        ],
                    }
                ],
                max_tokens=200
            )
            return response.choices[0].message.content.strip()

        except Exception as e:
            if "rate" in str(e).lower():
                time.sleep(2)
            else:
                return f"❌ OpenAI Error: {str(e)}"

    return "⚠️ Rate limit reached"