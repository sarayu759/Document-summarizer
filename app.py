import streamlit as st
import os
import base64

from utils.file_handler import extract_text
from utils.summarizer import summarize_multiple_documents
from utils.qa_engine import build_db, ask_question
from utils.llm import call_image_llm

st.title("📄 AI Document Summarizer + Q&A")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

if "text" not in st.session_state:
    st.session_state.text = ""

if "chunks" not in st.session_state:
    st.session_state.chunks = None


uploaded = st.file_uploader(
    "Upload files",
    accept_multiple_files=True,
    key="uploader_unique"
)

# -------- PROCESS FILES --------
if uploaded:
    texts = []

    for f in uploaded:
        path = os.path.join(UPLOAD_DIR, f.name)

        with open(path, "wb") as file:
            file.write(f.read())

        # PDF
        if f.name.endswith(".pdf"):
            texts.append(extract_text(path, "pdf"))

        # CSV
        elif f.name.endswith(".csv"):
            texts.append(extract_text(path, "csv"))

        # IMAGE
        elif f.name.lower().endswith((".png", ".jpg", ".jpeg")):
            with open(path, "rb") as img:
                base64_image = base64.b64encode(img.read()).decode()

            text = call_image_llm(base64_image)
            texts.append(text)

    st.session_state.text = "\n".join(texts)
    st.success("✅ Files processed")


# -------- TABS --------
tab1, tab2, tab3 = st.tabs(["Preview", "Summary", "Q&A"])

# Preview
with tab1:
    st.text_area("Preview", st.session_state.text[:2000], height=300)

# Summary
with tab2:
    if st.button("Generate Summary"):
        summary = summarize_multiple_documents(st.session_state.text)
        st.write(summary)

# Q&A
with tab3:
    if st.button("Enable Q&A"):
        st.session_state.chunks = build_db(st.session_state.text)
        st.success("Q&A Ready")

    question = st.text_input("Ask a question")

    if question and st.session_state.chunks:
        answer = ask_question(st.session_state.chunks, question)
        st.write(answer)