from services.transcript_service import TranscriptService

youtube_url = input("Enter YouTube URL: ")

transcript = TranscriptService.get_transcript(youtube_url)

print("\nTranscript Retrieved Successfully\n")

for item in transcript[:5]:
    print(item)