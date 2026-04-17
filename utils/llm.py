from groq import Groq
import streamlit as st

client = Groq(api_key=st.secrets["GROQ_API_KEY"])



def call_llm(prompt, max_tokens=300):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens
    )
    return response.choices[0].message.content.strip()