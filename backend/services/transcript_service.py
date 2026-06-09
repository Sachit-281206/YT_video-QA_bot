from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs


class TranscriptService:

    @staticmethod
    def extract_video_id(url: str) -> str:
        parsed_url = urlparse(url)

        if parsed_url.hostname == "youtu.be":
            return parsed_url.path[1:]

        if parsed_url.hostname in (
            "www.youtube.com",
            "youtube.com"
        ):
            return parse_qs(parsed_url.query)["v"][0]

        raise ValueError("Invalid YouTube URL")

    @staticmethod
    def get_transcript(youtube_url: str):
        video_id = TranscriptService.extract_video_id(youtube_url)

        api = YouTubeTranscriptApi()
        transcript = api.fetch(video_id)

        return transcript