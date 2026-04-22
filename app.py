import streamlit as st
import os

from utils.file_handler import extract_text
from utils.image_handler import extract_image_text
from utils.llm import call_llm
from utils.text_utils import chunk_text, get_relevant_chunks

st.set_page_config(page_title="AI Doc Summarizer", layout="wide")
st.title("📄 AI Document Summarizer + Q&A (FREE)")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

if "text" not in st.session_state:
    st.session_state.text = ""

if "chunks" not in st.session_state:
    st.session_state.chunks = []


# -------- FILE UPLOAD --------
uploaded_files = st.file_uploader("Upload PDF / CSV / Images", accept_multiple_files=True)

if uploaded_files:
    all_text = []

    for file in uploaded_files:
        path = os.path.join(UPLOAD_DIR, file.name)

        with open(path, "wb") as f:
            f.write(file.read())

        st.write(f"📄 Processing: {file.name}")

        if file.name.endswith(".pdf"):
            text = extract_text(path, "pdf")

        elif file.name.endswith(".csv"):
            text = extract_text(path, "csv")

        elif file.name.lower().endswith(("png", "jpg", "jpeg")):
            text = extract_image_text(path)

        else:
            text = ""

        all_text.append(text)

    st.session_state.text = "\n".join(all_text)
    st.session_state.chunks = chunk_text(st.session_state.text)

    st.success("✅ Files processed")


# -------- TABS --------
tab1, tab2, tab3 = st.tabs(["Preview", "Summary", "Q&A"])

# Preview
with tab1:
    st.text_area("Preview", st.session_state.text[:2000], height=300)

# Summary
with tab2:
    if st.button("Generate Summary"):
        if st.session_state.text:
            prompt = f"Summarize clearly:\n{st.session_state.text[:3000]}"
            st.write(call_llm(prompt))
        else:
            st.warning("Upload document first")

# Q&A
with tab3:
    question = st.text_input("Ask question")

    if question:
        chunks = get_relevant_chunks(st.session_state.chunks, question)
        context = "\n".join(chunks)

        prompt = f"""
Answer ONLY from context.

Context:
{context}

Question:
{question}
"""

        st.write(call_llm(prompt))