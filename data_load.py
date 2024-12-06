import pandas as pd

df = pd.read_json(
    "data/geopolitics/geopolitics_submissions.ndjson", lines=True)
print(df.head(10))
