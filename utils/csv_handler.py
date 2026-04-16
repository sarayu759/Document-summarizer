import pandas as pd

def extract_csv_text(path):
    try:
        df = pd.read_csv(path)

        # basic cleaning
        df = df.fillna("")

        # convert to structured text
        rows = []

        for _, row in df.iterrows():
            row_text = ", ".join([f"{col}: {row[col]}" for col in df.columns])
            rows.append(row_text)

        return "\n".join(rows[:200])  # limit rows

    except Exception as e:
        print("CSV error:", e)
        return ""