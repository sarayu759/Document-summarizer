import time
import os
import streamlit as st
from groq import Groq, RateLimitError, APIConnectionError
from dotenv import load_dotenv

# Load .env for local
load_dotenv()

# ---------------- API KEY HANDLING ----------------
def get_api_key():
    # Try Streamlit secrets (for deployment)
    try:
        return st.secrets["GROQ_API_KEY"]
    except:
        # fallback to .env (for local)
        return os.getenv("GROQ_API_KEY")


client = Groq(api_key=get_api_key())


# ---------------- LLM CALL ----------------
def call_llm(prompt, max_tokens=500):
    for _ in range(5):
        try:
            res = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens
            )
            return res.choices[0].message.content.strip()

        except (RateLimitError, APIConnectionError):
            time.sleep(2)

    return "⚠️ Error generating response"