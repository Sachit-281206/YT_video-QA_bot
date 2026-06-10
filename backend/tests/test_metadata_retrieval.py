from services.embedding_service import EmbeddingService
from services.vector_store_service import VectorStoreService


embedding_service = EmbeddingService()
vector_store = VectorStoreService()

question = input("Ask a question: ")

query_embedding = embedding_service.generate_embedding(
    question
).tolist()

results = vector_store.search(
    query_embedding=query_embedding,
    n_results=3
)

documents = results["documents"][0]
metadatas = results["metadatas"][0]

for i, (doc, metadata) in enumerate(
    zip(documents, metadatas),
    start=1
):
    print(f"\n--- Match {i} ---")

    print(
        f"Time: "
        f"{metadata['start_time']:.2f}s"
        f" -> "
        f"{metadata['end_time']:.2f}s"
    )

    print(doc[:300])