import streamlit as st
import os
from utils.file_handler import extract_text
from utils.summarizer import summarize_multiple_documents
from utils.qa_engine import build_db, ask_question

# ---------------- SESSION INIT ----------------
if "text" not in st.session_state:
    st.session_state.text = ""

if "db" not in st.session_state:
    st.session_state.db = None

UPLOAD_DIR = "uploaded_docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

st.title("📄 AI Document Summarizer + Q&A")

uploaded = st.file_uploader("Upload files", accept_multiple_files=True)
uploaded = st.file_uploader("Upload files", accept_multiple_files=True)

if uploaded:
    texts = []

    for f in uploaded:
        path = os.path.join(UPLOAD_DIR, f.name)

        with open(path, "wb") as file:
            file.write(f.read())

        # ---------------- PDF ----------------
        if f.name.endswith(".pdf"):
            text = extract_text(path, "pdf")
            if text:
                texts.append(text)

        # ---------------- CSV ----------------
        elif f.name.endswith(".csv"):
            text = extract_text(path, "csv")
            if text:
                texts.append(text)

        # ---------------- IMAGE (FIXED) ----------------
        elif f.name.lower().endswith((".png", ".jpg", ".jpeg")):
            import base64
            from utils.llm import call_vision_llm

            with open(path, "rb") as img:
                base64_image = base64.b64encode(img.read()).decode()

            st.info("🧠 Processing image with AI...")

            text = call_vision_llm(base64_image)

            if text:
                texts.append(text)
            else:
                texts.append("Image uploaded but no detailed description generated.")

    # ---------------- FINAL STORE ----------------
    if texts:
        st.session_state.text = "\n".join(texts)
        st.session_state.db = None
        st.success("✅ Document processed successfully")
    else:
        st.session_state.text = "No content extracted, but file uploaded."
        st.warning("⚠️ Could not extract structured text, but continuing.")