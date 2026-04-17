from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.llm import call_llm


def build_db(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )
    return splitter.split_text(text)


def ask_question(db, question):
    if not db:
        return "⚠️ No document loaded"

    relevant = []

    for chunk in db:
        if any(word.lower() in chunk.lower() for word in question.split()):
            relevant.append(chunk)

    if not relevant:
        relevant = db[:3]

    context = "\n\n".join(relevant[:4])

    return call_llm(f"""
Answer ONLY using this context.
If not found, say: Not found in document.

Context:
{context}

Question:
{question}
""", 300)