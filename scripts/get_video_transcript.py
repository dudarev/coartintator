"""
This script will get the transcript of a video from YouTube.
It uses https://github.com/jdepoix/youtube-transcript-api
"""

from youtube_transcript_api import YouTubeTranscriptApi

VIDEO_ID = "TRjq7t2Ms5I"
VIDEO_ID = "Y9qn4XGH1TI"
# VIDEO_ID = "kn5VfzQZajY"

LANGUAGES = [
    "en",
    "es",
    "uk",
    "ru",
]

transcript = YouTubeTranscriptApi.get_transcript(VIDEO_ID, languages=LANGUAGES)

text = "\n".join([line["text"] for line in transcript])
print(text)
