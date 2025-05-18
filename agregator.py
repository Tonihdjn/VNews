import torch
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, Filter
import numpy as np
from transformers import BertTokenizer, BertModel
from neo4j import GraphDatabase
# Initialize Qdrant client
client = QdrantClient(url="http://localhost:6333")  # Adjust URL if necessary
# Initialize Neo4j driver
uri = "bolt://localhost:7687"  # Neo4j connection URI (adjust if necessary)
username = "c2_userNamePlease"  # Your Neo4j username
password = "c2PasswordPlease"  # Your Neo4j password
driver = GraphDatabase.driver(uri, auth=(username, password))
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')
# Collection name
collection_name = "articles"
def generate_embedding(text):
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    # Take the [CLS] token (first token) embedding as sentence embedding
    embedding = outputs.last_hidden_state[:, 0, :].squeeze().numpy()
    return embedding
def fetchForId(q) : 
    qq = generate_embedding(qq)
    filter = {
        "must": [
            {"range": {"similarity_score": {"gte": 0.5}}}  # Optional filter: adjust based on your data
        ]
    }
    results = client.search(
        collection_name=collection_name,
        query_vector=qq,
        limit=10,  # Top-k results
        filter=filter,  # Optional filter
        with_payload=True  # Include metadata (e.g., article title) with the results
    )
    return results.id
def query(tx, q):
    # Use the transaction object (tx) to run a Cypher query
    tx.run(q)
