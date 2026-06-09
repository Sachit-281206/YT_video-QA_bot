from services.embedding_service import EmbeddingService
from services.vector_store_service import VectorStoreService
from services.qa_service import QAService


question = input("Ask a question: ")

embedding_service = EmbeddingService()
vector_store = VectorStoreService()
qa_service = QAService()

query_embedding = embedding_service.generate_embedding(
    question
).tolist()

results = vector_store.search(
    query_embedding=query_embedding,
    n_results=5
)

chunks = results["documents"][0]

print("\nRetrieved Chunks:\n")

documents = results["documents"][0]
distances = results["distances"][0]

for i, (chunk, distance) in enumerate(
    zip(documents, distances),
    start=1
):
    print(f"\n--- Chunk {i} ---")
    print(f"Distance: {distance}")
    print(chunk)
    
answer = qa_service.generate_answer(
    question,
    chunks
)

print("\nAnswer:\n")
print(answer)