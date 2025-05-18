import torch
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, Filter
import numpy as np
from transformers import BertTokenizer, BertModel
from neo4j import GraphDatabase
# --- Neo4j Graph Database Setup ---
uri = "bolt://localhost:7687"  # Sesuaikan dengan URI Neo4j Anda
username = "neo4j"
password = "password"

# --- Qdrant Vector Database Setup ---
client = QdrantClient(host="localhost", port=6333)

# Nama koleksi di Qdrant
collection_name = "articles"

# Membuat koneksi ke Neo4j
graph_db = GraphDatabase.driver(uri, auth=(username, password))
def fetch_graph_data():
    with graph_db.session() as session:
        query = """
        MATCH (p:Person)-[:WRITES]->(a:Article)
        RETURN p.name AS person_name, a.title AS article_title
        """
        result = session.run(query)
        return result
# Fungsi untuk melakukan pencarian vektor di Qdrant
def search_vector_db(query_vector, k=5):
    result = client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        top=k,
        with_payload=True
    )
    return result
