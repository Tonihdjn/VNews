from qdrant_client import QdrantClient, models

# Inisialisasi client untuk koneksi ke Qdrant
# Pastikan Qdrant berjalan di localhost:6333
client = QdrantClient(url="http://localhost:6333")

# Nama collection yang akan dibuat
collection_name = "articlesindex"

# Jalankan perintah untuk membuat (atau membuat ulang) collection
try:
    client.recreate_collection(
        collection_name=collection_name,
        # Konfigurasi untuk vektor
        vectors_config=models.VectorParams(
            size=384,
            distance=models.Distance.COSINE
        ),
        # Konfigurasi untuk HNSW (Hierarchical Navigable Small World) index
        hnsw_config=models.HnswConfigDiff(
            m=16,
            ef_construct=200
        )
    )
    print(f"✅ Collection '{collection_name}' berhasil dibuat/diperbarui.")

except Exception as e:
    print(f"❌ Terjadi error: {e}")