import pandas as pd
import torch
from transformers import BertTokenizer, BertModel
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
import json
from sentence_transformers import SentenceTransformer


model = SentenceTransformer('all-MiniLM-L6-v2')

# Function to generate embeddings using BERT
def generate_embedding(text):
    return model.encode(text)