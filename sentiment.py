from transformers import pipeline

import pandas
# Create a pipeline for sentiment analysis
classifier = pipeline("sentiment-analysis",
                      model="distilbert-base-uncased-finetuned-sst-2-english", device=0)
#cardiffnlp/twitter-roberta-base-sentiment-latest
#distilbert-base-uncased-finetuned-sst-2-english
#infile = "geopolitics"
infile = "combatfootage"
examples = True

if examples:
    limit = 10
else:
    limit = 1000000000
df = pandas.read_csv(f"./data/filtered_{infile}.csv")

upvotes_list = df["Upvotes"][0:limit]
text_list = df["Text"].tolist()[0:limit]
trunc_list = []
for entry in text_list:
    trunc_list.append(str(entry)[0:800])
# Analyze text
result = classifier(trunc_list, batch_size=1280)
print(result)

"""
with open("./data/results.csv", "wb") as f:
    """

df_out = pandas.DataFrame(data=result)
df_out["Upvotes"] = df["Upvotes"]
if examples:
    df_out["Text"] = df["Text"]
df_out.to_csv(f"./data/examples_{infile}.csv")