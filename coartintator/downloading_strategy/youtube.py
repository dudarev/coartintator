from urllib.parse import parse_qs, urlparse

from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi

from coartintator.downloading_strategy import AbstractDownloadingStrategy
from coartintator.entities import Post

LANGUAGES = [
    "es",
    "en",
    "uk",
    "ru",
]


def get_video_id(url: str) -> str | None:
    """
    This function will extract the video ID from a YouTube URL.
    """
    parsed_url = urlparse(url)
    if parsed_url.netloc == "youtu.be":
        return parsed_url.path[1:]
    if parsed_url.netloc in ("www.youtube.com", "youtube.com"):
        if parsed_url.path == "/watch":
            p = parse_qs(parsed_url.query)
            return p["v"][0]
        if parsed_url.path[:7] == "/embed/":
            return parsed_url.path.split("/")[2]
        if parsed_url.path[:3] == "/v/":
            return parsed_url.path.split("/")[2]
    return None


def get_video_transcript(url: str) -> str:
    """
    This script will get the transcript of a video from YouTube.
    It uses https://github.com/jdepoix/youtube-transcript-api
    """
    video_id = get_video_id(url)
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=LANGUAGES)
    return "\n".join([line["text"] for line in transcript])


def get_video_description(url: str) -> str:
    """
    Get video description from a YouTube.
    """
    video = YouTube(url)
    # as discussed at https://github.com/pytube/pytube/issues/1626
    video.streams.first()
    return video.description


CONTENT_TEMPLATE = """## Description
{description}

## Transcript

{transcript}
"""


class YouTubeDownloadingStrategy(AbstractDownloadingStrategy):
    def download(self, post) -> Post:
        post.content = CONTENT_TEMPLATE.format(
            description=get_video_description(post.url),
            transcript=get_video_transcript(post.url),
        )
        return post


class FakeYouTubeDownloadingStrategy(AbstractDownloadingStrategy):
    def download(self, post):
        # Simulate downloading by returning a static content or reading from a file
        post.content = "Fake transcript content"
        return post
