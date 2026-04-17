from utils.llm import call_llm

def summarize_text(text):
    prompt = f"""
Summarize the following document in clear bullet points:

{text[:3000]}
"""
    return call_llm(prompt, 400)


def summarize_multiple_documents(text):
    return summarize_text(text)