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
                "video_id": chunk["video_id"],
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
        video_id,
        n_results=5
    ):
        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where={
                "video_id": video_id
            },
            include=[
                "documents",
                "distances",
                "metadatas"
            ]
        )

    def count(self):
        return self.collection.count()
    
    def get_video_chunks(
        self,
        video_id
    ):

        results = self.collection.get(
            where={
                "video_id": video_id
            },
            include=[
                "documents",
                "metadatas"
            ]
        )

        return results