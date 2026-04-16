import time
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.llm import call_llm

def split_text(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )
    return splitter.split_text(text)

def map_step(chunks):
    results = []
    for c in chunks:
        time.sleep(0.3)
        results.append(call_llm(f"Summarize:\n{c}", 200))
    return results

def reduce_step(summaries):
    while len(summaries) > 5:
        new = []
        for i in range(0, len(summaries), 5):
            batch = summaries[i:i+5]
            combined = "\n\n".join(batch)
            new.append(call_llm(f"Combine:\n{combined}", 200))
        summaries = new

    final = "\n\n".join(summaries)
    return call_llm(f"""
Create final structured summary:

{final}

- Overview
- Key Points
- Insights
- Conclusion
""", 500)

def summarize_multiple_documents(texts):
    full = "\n\n".join(texts)

    if len(full) < 3000:
        return call_llm(f"Summarize clearly:\n{full}", 400)

    chunks = split_text(full)[:30]
    mapped = map_step(chunks)
    return reduce_step(mapped)