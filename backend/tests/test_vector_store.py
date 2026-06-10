from services.transcript_service import TranscriptService
from services.chunk_metadata_service import ChunkMetadataService
from services.embedding_service import EmbeddingService
from services.vector_store_service import VectorStoreService


youtube_url = input("Enter YouTube URL: ")

transcript = TranscriptService.get_transcript(
    youtube_url
)

chunks = (
    ChunkMetadataService
    .create_chunks_with_metadata(
        transcript
    )
)

embedding_service = EmbeddingService()

embeddings = [
    embedding_service.generate_embedding(
        chunk["text"]
    ).tolist()
    for chunk in chunks
]

vector_store = VectorStoreService()

vector_store.add_documents(
    chunks,
    embeddings
)

print(
    f"\nStored Chunks: {vector_store.count()}"
)