import hashlib
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue
)

class QdrantStore:
    def __init__(self, url: str, collection: str, vector_dim: int):
        self.client = QdrantClient(url=url)
        self.collection = collection
        self.vector_dim = vector_dim
        self._ensure_collection()

    def _ensure_collection(self):
        if not self.client.collection_exists(self.collection):
            self.client.create_collection(
                collection_name=self.collection,
                vectors_config=VectorParams(
                    size=self.vector_dim,
                    distance=Distance.COSINE
                )
            )

    def _generate_id(self, text: str, source: str):
        return hashlib.md5((text + source).encode()).hexdigest()

    def upsert(self, embeddings, texts, metadata):
        points = []
        for emb, text, meta in zip(embeddings, texts, metadata):
            points.append(
                PointStruct(
                    id=self._generate_id(text, meta["source"]),
                    vector=emb,
                    payload={"text": text, **meta}
                )
            )
        self.client.upsert(self.collection, points)

    def search(self, query_embedding, limit=5):
        return self.client.search(
            collection_name=self.collection,
            query_vector=query_embedding,
            limit=limit
        )

    def delete_file(self, filename: str):
        self._ensure_collection()

        self.client.delete(
            collection_name=self.collection,
            points_selector=Filter(
                must=[
                    FieldCondition(
                        key="source",
                        match=MatchValue(value=filename)
                    )
                ]
            )
        )

    def reset(self):
        self.client.delete_collection(self.collection)
        self._ensure_collection()