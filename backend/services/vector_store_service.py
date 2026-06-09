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

        documents = [
            chunk["text"]
            for chunk in chunks
        ]

        metadatas = [
            {
                "start_time": chunk["start_time"],
                "end_time": chunk["end_time"]
            }
            for chunk in chunks
        ]

        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )

    def search(
        self,
        query_embedding,
        n_results=5
    ):
        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            include=[
                "documents",
                "distances",
                "metadatas"
            ]
        )

    def count(self):
        return self.collection.count()