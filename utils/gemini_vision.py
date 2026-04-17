import streamlit as st
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-pro-vision")


def analyze_image(image_path):
    try:
        image = Image.open(image_path)

        response = model.generate_content([
            "Describe this image clearly. Extract all text and summarize.",
            image
        ])

        return response.text

    except Exception as e:
        return f"❌ Gemini Error: {str(e)}"