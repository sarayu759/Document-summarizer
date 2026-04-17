import streamlit as st
import os
import base64
from utils.file_handler import extract_text
from utils.summarizer import summarize_multiple_documents
from utils.qa_engine import build_db, ask_question
from utils.llm import call_vision_llm

# ---------------- SESSION ----------------
if "text" not in st.session_state:
    st.session_state.text = ""

if "db" not in st.session_state:
    st.session_state.db = None

UPLOAD_DIR = "uploaded_docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

st.title("📄 AI Document Summarizer + Q&A")

# ✅ FIXED DUPLICATE ERROR
uploaded = st.file_uploader(
    "Upload files",
    accept_multiple_files=True,
    key="file_uploader_main"
)

# ---------------- PROCESS FILES ----------------
if uploaded:
    texts = []

    for f in uploaded:
        path = os.path.join(UPLOAD_DIR, f.name)

        with open(path, "wb") as file:
            file.write(f.read())

        # -------- PDF --------
        if f.name.endswith(".pdf"):
            text = extract_text(path, "pdf")
            if text:
                texts.append(text)

        # -------- CSV --------
        elif f.name.endswith(".csv"):
            text = extract_text(path, "csv")
            if text:
                texts.append(text)

        # -------- IMAGE (VISION MODEL) --------
        elif f.name.lower().endswith((".png", ".jpg", ".jpeg")):
            with open(path, "rb") as img:
                base64_image = base64.b64encode(img.read()).decode()

            st.info("🧠 Processing image with AI...")

            text = call_vision_llm(base64_image)

            if text:
                texts.append(text)
            else:
                texts.append("Image uploaded but no detailed description generated.")

    # -------- FINAL STORE --------
    if texts:
        st.session_state.text = "\n".join(texts)
        st.session_state.db = None
        st.success("✅ Document processed successfully")
    else:
        st.session_state.text = "No content extracted, but file uploaded."
        st.warning("⚠️ Could not extract structured text, continuing.")

# ---------------- TABS ----------------
tab1, tab2, tab3 = st.tabs(["Preview", "Summary", "Q&A"])

# -------- PREVIEW --------
with tab1:
    if st.session_state.text:
        st.text_area("Preview", st.session_state.text[:2000], height=300)

# -------- SUMMARY --------
with tab2:
    if st.button("Generate Summary"):
        if not st.session_state.text:
            st.error("⚠️ Upload document first")
        else:
            summary = summarize_multiple_documents(st.session_state.text)
            st.write(summary)

# -------- Q&A --------
with tab3:
    if st.button("Enable Q&A"):
        if not st.session_state.text:
            st.error("⚠️ Upload document first")
        else:
            st.session_state.db = build_db(st.session_state.text)
            st.success("Q&A Ready")

    q = st.text_input("Ask a question")

    if q:
        if not st.session_state.db:
            st.warning("⚠️ Enable Q&A first")
        else:
            answer = ask_question(st.session_state.db, q)
            st.write(answer)