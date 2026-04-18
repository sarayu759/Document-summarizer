import streamlit as st
import os
import base64
from PIL import Image
import io

from utils.file_handler import extract_text
from utils.summarizer import summarize_multiple_documents
from utils.qa_engine import build_db, ask_question
from utils.llm import call_image_llm
from utils.image_handler import extract_image_text

st.set_page_config(page_title="AI Doc Summarizer", layout="wide")

st.title("📄 AI Document Summarizer + Q&A")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

if "text" not in st.session_state:
    st.session_state.text = ""

if "db" not in st.session_state:
    st.session_state.db = None


def compress_image(path):
    img = Image.open(path).convert("RGB")
    img = img.resize((512, 512))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()


uploaded = st.file_uploader(
    "Upload files",
    accept_multiple_files=True,
    key="unique_uploader"
)

# -------- PROCESS --------
if uploaded:
    texts = []

    for f in uploaded:
        path = os.path.join(UPLOAD_DIR, f.name)

        with open(path, "wb") as file:
            file.write(f.read())

        if f.name.endswith(".pdf"):
            texts.append(extract_text(path, "pdf"))

        elif f.name.endswith(".csv"):
            texts.append(extract_text(path, "csv"))

        elif f.name.lower().endswith((".png", ".jpg", ".jpeg")):

            base64_img = compress_image(path)

            st.info("🧠 Processing image...")

            text = call_image_llm(base64_img)

            # fallback if API fails
            if not text or "error" in text.lower():
                text = extract_image_text(path)

            texts.append(text)

    st.session_state.text = "\n".join(texts)
    st.success("✅ Files processed")


# -------- UI --------
tab1, tab2, tab3 = st.tabs(["Preview", "Summary", "Q&A"])

with tab1:
    st.text_area("Preview", st.session_state.text[:2000], height=300)

with tab2:
    if st.button("Generate Summary"):
        if st.session_state.text:
            st.write(summarize_multiple_documents(st.session_state.text))
        else:
            st.warning("⚠️ Upload document first")

with tab3:
    if st.button("Enable Q&A"):
        if st.session_state.text:
            st.session_state.db = build_db(st.session_state.text)
            st.success("Q&A Ready")
        else:
            st.warning("⚠️ Upload document first")

    q = st.text_input("Ask question")

    if q and st.session_state.db:
        st.write(ask_question(st.session_state.db, q))