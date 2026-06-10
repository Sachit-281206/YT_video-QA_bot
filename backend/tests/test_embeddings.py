from services.embedding_service import EmbeddingService

embedding_service = EmbeddingService()

text = "What is Retrieval Augmented Generation?"

embedding = embedding_service.generate_embedding(text)

print(f"Vector Dimension: {len(embedding)}")

print("\nFirst 10 values:\n")

print(embedding[:10])