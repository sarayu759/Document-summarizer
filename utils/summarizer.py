from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.llm import call_llm


def summarize_text(text, mode="Detailed"):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_text(text)

    summaries = []

    for chunk in chunks:
        if mode == "Short":
            prompt = f"Give a short summary:\n{chunk}"
        else:
            prompt = f"""
            Summarize the text with:
            - Key Points
            - Important Insights
            - Final Summary

            Text:
            {chunk}
            """

        result = call_llm(prompt)
        summaries.append(result)

    return "\n\n".join(summaries)