import streamlit as st
import os
from utils.file_handler import extract_text
from utils.summarizer import summarize_multiple_documents
from utils.qa_engine import build_db, ask_question

st.set_page_config(page_title="AI Doc Agent", layout="wide")

st.title("📄 AI Document Intelligence System")

UPLOAD_DIR = "uploaded_docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

if "text" not in st.session_state:
    st.session_state.text = ""

if "db" not in st.session_state:
    st.session_state.db = None

if "chat" not in st.session_state:
    st.session_state.chat = []

uploaded = st.sidebar.file_uploader(
    "Upload files",
    type=["pdf", "csv", "png", "jpg", "jpeg"],
    accept_multiple_files=True
)

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

        st.write(f"📄 Extracted from {f.name}:", text[:300])

        if text.strip():
            texts.append(text)

    st.session_state.text = "\n\n".join(texts)

tabs = st.tabs(["Preview", "Summary", "Q&A"])

with tabs[0]:
    st.text_area("Preview", st.session_state.text[:5000], height=400)

with tabs[1]:
    if st.button("Generate Summary"):
        st.write(summarize_multiple_documents([st.session_state.text]))

with tabs[2]:
    if st.button("Enable Q&A"):
        st.session_state.db = build_db(st.session_state.text)
        st.success("Q&A Ready")

    q = st.text_input("Ask a question")

    if q:
        if st.session_state.db is None:
            st.warning("Click Enable Q&A first")
        else:
            ans = ask_question(st.session_state.db, q)
            st.session_state.chat.append((q, ans))

    for q, a in st.session_state.chat:
        st.write("🧑", q)
        st.write("🤖", a)