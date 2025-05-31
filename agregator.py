# from neo4j import GraphDatabase
# from qdrant_client import QdrantClient
# import numpy as np

# uri = "bolt://localhost:7687"
# username = "neo4j"
# password = "Pumkin!!22"

# client = QdrantClient(host="localhost", port=6333)
# collection_name = "article's"

# graph_db = GraphDatabase.driver(uri, auth=(username, password))

# def fetch_graph_data(query):
#     with graph_db.session() as session:
#         result = session.run(query)
#         return [record.data() for record in result]

# def search_vector_db(query_vector, k=5):
#     # Pencarian dengan index Qdrant
#     result = client.search(
#         collection_name=collection_name,
#         query_vector=query_vector,
#         limit=k,
#         with_payload=True
#     )
#     return result

# def search_vector_db_no_index(query_vector, k=5):
#     import numpy as np

#     all_points = []

#     for batch in client.scroll(collection_name=collection_name, with_vectors=True, with_payload=True):
#         points_batch = getattr(batch, "points", None)
#         if points_batch is not None:
#             all_points.extend(points_batch)
#         elif isinstance(batch, list):
#             all_points.extend(batch)
#         else:
#             all_points.append(batch)

#     vectors = []
#     payloads = []
#     ids = []

#     for pt in all_points:
#         # pastikan pt bukan int, dan punya atribut vector
#         if hasattr(pt, "vector") and hasattr(pt, "payload") and hasattr(pt, "id"):
#             vectors.append(pt.vector)
#             payloads.append(pt.payload)
#             ids.append(pt.id)
#         else:
#             # skip item yang bukan objek point valid
#             continue

#     vectors = np.array(vectors)
#     query_vec = np.array(query_vector)

#     def cosine_sim(a, b):
#         return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

#     sims = np.array([cosine_sim(query_vec, v) for v in vectors])

#     topk_idx = sims.argsort()[-k:][::-1]

#     results = []
#     for idx in topk_idx:
#         results.append(
#             type("Result", (), {
#                 "id": ids[idx],
#                 "score": float(sims[idx]),
#                 "payload": payloads[idx]
#             })()
#         )

#     return results

from neo4j import GraphDatabase
from qdrant_client import QdrantClient
import numpy as np

uri = "bolt://localhost:7687"
username = "neo4j"
password = "Pumkin!!22"

client = QdrantClient(host="localhost", port=6333)
collection_name = "article's"

graph_db = GraphDatabase.driver(uri, auth=(username, password))

def fetch_graph_data(query, params=None):
    with graph_db.session() as session:
        result = session.run(query, parameters=params or {})
        return [record.data() for record in result]

def search_vector_db(query_vector, k=5):
    result = client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=k,
        with_payload=True
    )
    return result

def search_vector_db_no_index(query_vector, k=5):
    all_points = []

    for batch in client.scroll(collection_name=collection_name, with_vectors=True, with_payload=True):
        points_batch = getattr(batch, "points", None)
        if points_batch is not None:
            all_points.extend(points_batch)
        elif isinstance(batch, list):
            all_points.extend(batch)
        else:
            all_points.append(batch)

    vectors = []
    payloads = []
    ids = []

    for pt in all_points:
        if hasattr(pt, "vector") and hasattr(pt, "payload") and hasattr(pt, "id"):
            vectors.append(pt.vector)
            payloads.append(pt.payload)
            ids.append(pt.id)

    vectors = np.array(vectors)
    query_vec = np.array(query_vector)

    def cosine_sim(a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    sims = np.array([cosine_sim(query_vec, v) for v in vectors])

    topk_idx = sims.argsort()[-k:][::-1]

    results = []
    for idx in topk_idx:
        results.append(
            type("Result", (), {
                "id": ids[idx],
                "score": float(sims[idx]),
                "payload": payloads[idx]
            })()
        )

    return results

def check_vector_exists(id):
    # Panggil retrieve Qdrant untuk cek ada id-nya
    result = client.retrieve(collection_name=collection_name, ids=[id])
    return len(result) > 0