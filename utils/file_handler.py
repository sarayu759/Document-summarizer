import pandas as pd
from pypdf import PdfReader


def extract_text(path, filetype):
    if filetype == "pdf":
        reader = PdfReader(path)
        return "".join([p.extract_text() or "" for p in reader.pages])

    elif filetype == "csv":
        df = pd.read_csv(path)
        return df.to_string()

    return ""