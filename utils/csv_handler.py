import pandas as pd

def extract_csv_text(path):
    df = pd.read_csv(path)
    return df.to_string()