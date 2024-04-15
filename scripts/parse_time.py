"""
This script demonstrates how to parse a time string and convert it to a specific timezone.
"""

import dateparser
import pytz

time_string = "12 hours ago"
parsed_time = dateparser.parse(time_string)

# If you want to convert the parsed time to UTC
utc_time = parsed_time.astimezone(tz=pytz.UTC)

print(parsed_time)
print(utc_time)
