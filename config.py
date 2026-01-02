# config.py

# OAuth
CLIENT_SECRETS_FILE = "yt_upload.json"
TOKEN_FILE = "token.json"

# YouTube API
YOUTUBE_UPLOAD_SCOPE = ["https://www.googleapis.com/auth/youtube.upload"]
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# Video settings
VIDEO_CATEGORY = "15"
PRIVACY_STATUS = "private"

# Paths
VIDEO_DIRECTORY = "videos"
CSV_FILE = "video_metadata.csv"

# Scheduling
SET_SIZE = 5
START_DATE = "2025-04-26"

# UTC Timings
SCHEDULE_TIMINGS = [
    (23, 0),
    (23, 30),
    (0, 0),
    (0, 30),
    (1, 0),
    (1, 30),
    (2, 0),
    (2, 30),
    (3, 0),
    (3, 30),
]
