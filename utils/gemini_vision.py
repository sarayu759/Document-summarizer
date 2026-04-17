import streamlit as st
import google.generativeai as genai

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-1.5-flash")

def analyze_image(image_path):
    with open(image_path, "rb") as f:
        image_bytes = f.read()

    response = model.generate_content([
        "Analyze this image and extract all useful information. Give summary and key points.",
        {"mime_type": "image/png", "data": image_bytes}
    ])

    return response.text