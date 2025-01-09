from transformers import pipeline, AutoTokenizer

import pandas
# Create a pipeline for sentiment analysis
model_name = "distilbert-base-uncased-finetuned-sst-2-english"
tokenizer = AutoTokenizer.from_pretrained(model_name, model_max_length=512)
classifier = pipeline("sentiment-analysis",
                      model=model_name, device=0, tokenizer=tokenizer)
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
#token_batch = tokenizer(text_list, max_length=512)
#token_list = [ token_batch.tokens(i) for i in range(len(text_list)) ]
# Analyze text
result = classifier(text_list, batch_size=1280)
print(result)

"""
with open("./data/results.csv", "wb") as f:
    """

df_out = pandas.DataFrame(data=result)
df_out["Upvotes"] = df["Upvotes"]
if examples:
    df_out["Text"] = df["Text"]
df_out.to_csv(f"./data/examples_{infile}.csv")
