from transformers import pipeline

import pandas
# Create a pipeline for sentiment analysis
classifier = pipeline("sentiment-analysis",
                      model="distilbert-base-uncased-finetuned-sst-2-english", device=0)
#cardiffnlp/twitter-roberta-base-sentiment-latest
#distilbert-base-uncased-finetuned-sst-2-english
#infile = "geopolitics"
infile = "geopolitics"
df = pandas.read_csv(f"./data/filtered_{infile}.csv")

upvotes_list = df["Upvotes"]
text_list = df["Text"].tolist()
trunc_list = []
for entry in text_list:
    trunc_list.append(str(entry)[0:800])
# Analyze text
result = classifier(trunc_list, batch_size=128)
print(result)

"""
with open("./data/results.csv", "wb") as f:
    """

df_out = pandas.DataFrame(data=result)
df_out["Upvotes"] = df["Upvotes"]

df_out.to_csv(f"./data/results_{infile}.csv")
