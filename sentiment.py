from transformers import pipeline

# Create a pipeline for sentiment analysis
classifier = pipeline("sentiment-analysis",
                      model="distilbert-base-uncased-finetuned-sst-2-english")

# Analyze text
result = classifier("I love programming with Python!")
print(result)
