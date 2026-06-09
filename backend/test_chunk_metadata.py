from services.transcript_service import TranscriptService
from services.chunk_metadata_service import (
    ChunkMetadataService
)

youtube_url = input(
    "Enter YouTube URL: "
)

transcript = TranscriptService.get_transcript(
    youtube_url
)

chunks = (
    ChunkMetadataService
    .create_chunks_with_metadata(
        transcript
    )
)

print()

print(chunks[0])