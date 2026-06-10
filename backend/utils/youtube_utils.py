from urllib.parse import (
    urlparse,
    parse_qs
)


def extract_video_id(
    youtube_url: str
):
    parsed = urlparse(
        youtube_url
    )

    if parsed.hostname == "youtu.be":
        return parsed.path[1:]

    if (
        parsed.hostname ==
        "www.youtube.com"
        or
        parsed.hostname ==
        "youtube.com"
    ):
        return parse_qs(
            parsed.query
        )["v"][0]

    return None

import yt_dlp


def get_video_title(
    youtube_url: str
):

    ydl_opts = {
        "quiet": True,
        "skip_download": True
    }

    with yt_dlp.YoutubeDL(
        ydl_opts
    ) as ydl:

        info = ydl.extract_info(
            youtube_url,
            download=False
        )

        return info["title"]