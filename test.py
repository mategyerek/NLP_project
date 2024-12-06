import torch
# Download vocabulary from S3 and cache.
tokenizer = torch.hub.load(
    'huggingface/pytorch-transformers', 'tokenizer', 'bert-base-uncased')
