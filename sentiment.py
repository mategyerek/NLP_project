from transformers import pipeline

import pandas
# Create a pipeline for sentiment analysis
model_name = "distilbert-base-uncased-finetuned-sst-2-english"
classifier = pipeline("sentiment-analysis",
                      model=model_name, device=0)
#cardiffnlp/twitter-roberta-base-sentiment-latest
#distilbert-base-uncased-finetuned-sst-2-english
#infile = "geopolitics"
infile = "combatfootage"
examples = False

if examples:
    limit = 10
else:
    limit = 1000000000
df = pandas.read_csv(f"./data/filtered_{infile}.csv")

upvotes_list = df["Upvotes"][0:limit]
text_list = df["Text"].tolist()[0:limit]
#token_batch = tokenizer(text_list, max_length=512)
#token_list = [ token_batch.tokens(i) for i in range(len(text_list)) ]
# Analyze text
trunc_list = []
for entry in text_list:
    trunc_list.append(str(entry)[0:800])

result = classifier(trunc_list, batch_size=64)
print(result)

"""
with open("./data/results.csv", "wb") as f:
    """

df_out = pandas.DataFrame(data=result)
df_out["Upvotes"] = df["Upvotes"]
if examples:
    df_out["Text"] = df["Text"]
df_out.to_csv(f"./data/examples_{infile}.csv")
