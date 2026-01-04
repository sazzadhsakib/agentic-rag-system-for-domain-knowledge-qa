class Retriever:
    def __init__(self, store, embedder):
        self.store = store
        self.embedder = embedder

    def retrieve(self, query: str, top_k: int):
        query_embedding = self.embedder.embed([query])[0]
        hits = self.store.search(query_embedding, limit=top_k)

        return [
            {
                "text": hit.payload["text"],
                "source": hit.payload.get("source")
            }
            for hit in hits
        ]
