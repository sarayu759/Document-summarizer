from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from utils.llm import call_llm


def build_db(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split_text(text)

    embedding = OpenAIEmbeddings()
    db = Chroma.from_texts(chunks, embedding)

    return db


def ask_question(db, question):
    retriever = db.as_retriever(search_kwargs={"k": 3})
    docs = retriever.get_relevant_documents(question)

    context = "\n".join([doc.page_content for doc in docs])

    prompt = f"""
    Answer ONLY from the context.
    If not found, say "Not found in document".

    Context:
    {context}

    Question:
    {question}
    """

    answer = call_llm(prompt)

    return f"""
    Answer:
    {answer}

    -------------------
    Source:
    {context}
    """