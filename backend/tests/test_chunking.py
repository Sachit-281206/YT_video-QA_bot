from services.transcript_service import TranscriptService
from services.chunk_service import ChunkService

youtube_url = input("Enter YouTube URL: ")

transcript = TranscriptService.get_transcript(youtube_url)

# Convert transcript snippets into one large text
full_text = " ".join(
    snippet.text
    for snippet in transcript
)

chunks = ChunkService.create_chunks(full_text)

print(f"\nTotal Chunks: {len(chunks)}\n")

for i, chunk in enumerate(chunks[:3], start=1):
    print(f"\n----- Chunk {i} -----\n")
    print(chunk[:500])