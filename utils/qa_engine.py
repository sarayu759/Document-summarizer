from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.llm import call_llm


def build_db(text):
    if not text.strip():
        return []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )

    chunks = splitter.split_text(text)

    return chunks


def ask_question(db, question):
    if not db:
        return "⚠️ No document loaded"

    # simple keyword matching (lightweight retrieval)
    relevant_chunks = []

    for chunk in db:
        if any(word.lower() in chunk.lower() for word in question.split()):
            relevant_chunks.append(chunk)

    if not relevant_chunks:
        relevant_chunks = db[:3]  # fallback

    context = "\n\n".join(relevant_chunks[:4])

    return call_llm(f"""
You are a precise assistant.

Answer ONLY using the context below.
Do NOT guess.
If answer not present, say: "Not found in document".

Context:
{context}

Question:
{question}

Give a clear and concise answer.
""", 400)