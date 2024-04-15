"""
Get video description from a YouTube.
"""

from pytube import YouTube

VIDEO_URL = "https://www.youtube.com/watch?v=Ou94Bmjp-dg&ab_channel=Every"
VIDEO_ID = "Ou94Bmjp-dg"

video = YouTube(VIDEO_URL)
# as discussed at https://github.com/pytube/pytube/issues/1626
stream = video.streams.first()
print(video.description)
