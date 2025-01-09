from transformers import pipeline
import pandas
# Create a pipeline for sentiment analysis
classifier = pipeline("sentiment-analysis",
                      model="distilbert-base-uncased-finetuned-sst-2-english", device="cuda:0")
df = pandas.read_csv("./data/geopolitics_parent_child.csv")
text_list = df["Text"].tolist()
trunc_list = []
for entry in text_list:
    trunc_list.append(entry[0:512])
# Analyze text
result = classifier(trunc_list)
print(result)
