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

print("\nTop Matches:\n")

for i, doc in enumerate(results["documents"][0], start=1):
    print(f"\n--- Match {i} ---\n")
    print(doc[:500])