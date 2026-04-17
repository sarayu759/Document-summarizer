from utils.llm import call_llm

def summarize_multiple_documents(text):
    prompt = f"""
Summarize clearly in bullet points:

{text[:3000]}
"""
    return call_llm(prompt, 300)