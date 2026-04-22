def chunk_text(text, size=500):
    return [text[i:i+size] for i in range(0, len(text), size)]


def get_relevant_chunks(chunks, question):
    relevant = []

    for chunk in chunks:
        if any(word.lower() in chunk.lower() for word in question.split()):
            relevant.append(chunk)

    return relevant[:3] if relevant else chunks[:3]