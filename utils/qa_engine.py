from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.llm import call_llm

def build_db(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )
    return splitter.split_text(text)


def ask_question(chunks, question):
    context = "\n\n".join(chunks[:4])

    prompt = f"""
Answer from context only.

Context:
{context}

Question:
{question}
"""
    return call_llm(prompt, 200)