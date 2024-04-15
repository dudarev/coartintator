"""
Get videos from a YouTube channel.
"""

# from pprint import pprint
import scrapetube

CHANNEL_URL = "https://www.youtube.com/@ArtemDudarev"
# CHANNEL_URL = "https://www.youtube.com/@EveryInc"

# videos = scrapetube.get_channel(channel_url=CHANNEL_URL)
videos = scrapetube.get_channel(channel_url=CHANNEL_URL, content_type="streams")

for video in videos:
    print(video["title"]["runs"][0]["text"])
    print(video["videoId"])
    # pprint(video, indent=2)
