from qdrant_client import QdrantClient, models

client = QdrantClient(url="http://localhost:6333")
collection_name = "article's"

client.recreate_collection(
    collection_name=collection_name,
    vectors_config=models.VectorParams(
        size=384,
        distance=models.Distance.COSINE
    )
    # Perhatikan: kita tidak menyertakan parameter hnsw_config
)
print(f"Collection '{collection_name}' berhasil dibuat.")