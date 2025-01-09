from transformers import pipeline
import pandas
# Create a pipeline for sentiment analysis
classifier = pipeline("sentiment-analysis",
                      model="distilbert-base-uncased-finetuned-sst-2-english", device=-1)

limit = 100000000
infile = "geopolitics"

df = pandas.read_csv(f"./data/{infile}_parent_child.csv")

upvotes_list = df["Upvotes"][0:limit]
text_list = df["Text"].tolist()[0:limit]
trunc_list = []
for entry in text_list:
    trunc_list.append(entry[0:512])
# Analyze text
result = classifier(trunc_list)
print(result)

"""
with open("./data/results.csv", "wb") as f:
    """

df_out = pandas.DataFrame(data=result)
df_out["Upvotes"] = df["Upvotes"]

df_out.to_csv(f"./data/results_{infile}.csv")
