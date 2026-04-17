from utils.llm import call_llm


def summarize_multiple_documents(text):
    if len(text) < 3000:
        return call_llm(f"Summarize this:\n{text}", 400)

    # chunking
    chunks = [text[i:i+2000] for i in range(0, len(text), 2000)]

    summaries = []

    for c in chunks:
        s = call_llm(f"Summarize this:\n{c}", 200)
        summaries.append(s)

    final = "\n".join(summaries)

    return call_llm(f"Combine into final summary:\n{final}", 400)