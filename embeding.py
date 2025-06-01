import pandas as pd
import torch
from transformers import BertTokenizer, BertModel
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
import json
from sentence_transformers import SentenceTransformer


client = QdrantClient(url="http://localhost:6333")  # Adjust URL if necessary

model = SentenceTransformer('all-MiniLM-L6-v2')

# Function to generate embeddings using BERT
def generate_embedding(text):
    return model.encode(text)

# Load pre-trained BERT model

# Initialize Qdrant clie

# Recreate collection with vector configuration
collection_name = "article's"


articles = pd.read_csv('vector_dataFinal.csv')

def convert_id(id):
    return int(id)

# Embed articles and add them to Qdrant
for _, row in articles.iterrows():  # articles is a dataframe
    text = f"{row['headline']} {row['category']} {row.get('short_desc', '')}"
    id_ = int(row['id_artikel'])
    embedding = generate_embedding(text)  # should return numpy array or list

    point = PointStruct(
        id=id_,
        vector=embedding.tolist() if hasattr(embedding, 'tolist') else embedding,
        payload={
            "headline": row['headline'],
            "category": row['category'],
            "short_desc": row.get('short_desc', '')
        }
    )

    client.upsert(
        collection_name=collection_name,
        points=[point]
    )



print("Articles have been successfully embedded and uploaded to Qdrant.")
