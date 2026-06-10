from services.embedding_service import EmbeddingService
from services.vector_store_service import VectorStoreService
# from services.qa_service_gemini import QAService
from services.qa_service_ollama import QAService
from utils.time_utils import seconds_to_mmss


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

documents = results["documents"][0]
distances = results["distances"][0]
metadatas = results["metadatas"][0]

print("\nRetrieved Chunks:\n")

for i, (chunk, distance, metadata) in enumerate(
    zip(documents, distances, metadatas),
    start=1
):
    print(f"\n--- Chunk {i} ---")
    print(f"Distance: {distance:.4f}")

    start_time = seconds_to_mmss(
        metadata["start_time"]
    )

    end_time = seconds_to_mmss(
        metadata["end_time"]
    )

    print(
        f"Timestamp: "
        f"{start_time} - {end_time}"
    )

    print(chunk[:500])

answer = qa_service.generate_answer(
    question,
    documents
)

print("\n" + "=" * 50)
print("ANSWER")
print("=" * 50)

print(answer)

print("\n" + "=" * 50)
print("SOURCES")
print("=" * 50)

for metadata in metadatas:

    start_time = seconds_to_mmss(
        metadata["start_time"]
    )

    end_time = seconds_to_mmss(
        metadata["end_time"]
    )

    print(
        f"{start_time} - {end_time}"
    )