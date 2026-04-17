from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.llm import call_llm


def build_db(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )
    return splitter.split_text(text)


def ask_question(chunks, question):
    context = "\n\n".join(chunks[:4])

    prompt = f"""
Answer ONLY using this context.
If not found, say "Not found in document".

Context:
{context}

Question:
{question}
"""
    return call_llm(prompt, 300)