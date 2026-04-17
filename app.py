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

# ---------------- FILE PROCESS ----------------
if uploaded:
    texts = []

    for f in uploaded:
        path = os.path.join(UPLOAD_DIR, f.name)

        with open(path, "wb") as file:
            file.write(f.read())

        if f.name.endswith(".pdf"):
            text = extract_text(path, "pdf")

        elif f.name.endswith(".csv"):
            text = extract_text(path, "csv")

        elif f.name.lower().endswith((".png", ".jpg", ".jpeg")):
            text = extract_text(path, "image")

        else:
            text = ""

        if text:
            texts.append(text)

    if texts:
        st.session_state.text = "\n".join(texts)
        st.session_state.db = None
        st.success("✅ Document loaded successfully")
    else:
        st.session_state.text = ""
        st.error("❌ Could not extract content from file")

# ---------------- TABS ----------------
tab1, tab2, tab3 = st.tabs(["Preview", "Summary", "Q&A"])

# ---------------- PREVIEW ----------------
with tab1:
    if st.session_state.text:
        st.text_area("Preview", st.session_state.text[:2000], height=300)

# ---------------- SUMMARY ----------------
with tab2:
    if st.button("Generate Summary"):
        if not st.session_state.text:
            st.error("⚠️ Upload a document first")
        else:
            summary = summarize_multiple_documents(st.session_state.text)
            st.write(summary)

# ---------------- Q&A ----------------
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