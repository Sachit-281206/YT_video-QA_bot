import chromadb


class VectorStoreService:

    def __init__(self):
        self.client = chromadb.PersistentClient(
            path="../chroma_db"
        )

        self.collection = self.client.get_or_create_collection(
            name="youtube_chunks"
        )

    def add_documents(
        self,
        chunks,
        embeddings
    ):
        ids = [
            f"chunk_{i}"
            for i in range(len(chunks))
        ]

        self.collection.add(
            ids=ids,
            documents=chunks,
            embeddings=embeddings
        )

    def search(
        self,
        query_embedding,
        n_results=5
    ):
        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            include=["documents", "distances"]
        )

    def count(self):
        return self.collection.count()