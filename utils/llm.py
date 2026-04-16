import streamlit as st
from groq import Groq


def get_api_key():
    return st.secrets["GROQ_API_KEY"]


client = Groq(api_key=get_api_key())


def call_llm(prompt, max_tokens=300):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens
    )
    return response.choices[0].message.content.strip()