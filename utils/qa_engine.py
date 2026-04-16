from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.llm import call_llm

embeddings = HuggingFaceEmbeddings()


def build_db(text):
    if not text.strip():
        return None

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )

    chunks = splitter.split_text(text)

    return Chroma.from_texts(chunks, embeddings)


def ask_question(db, question):
    if db is None:
        return "⚠️ No document loaded"

    docs = db.similarity_search(question, k=4)

    if not docs:
        return "⚠️ No relevant content found"

    context = "\n\n".join([d.page_content for d in docs])

    return call_llm(f"""
Answer ONLY using this context.
If not found, say "Not found in document".

Context:
{context}

Question:
{question}
""", 400)