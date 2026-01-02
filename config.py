# config.py

# OAuth
CLIENT_SECRETS_FILE = "yt_upload.json"
YOUTUBE_TOKEN_FILE = "tokens/youtube/token.json"
SHEET_TOKEN_FILE = "tokens/sheets/token.json"

# YouTube API
YOUTUBE_UPLOAD_SCOPE = ["https://www.googleapis.com/auth/youtube.upload",
                        "https://www.googleapis.com/auth/youtube",
                        ]

SHEET_AND_DRIVE_SCOPE =[
     "https://www.googleapis.com/auth/spreadsheets",
     "https://www.googleapis.com/auth/drive"
]
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


# Paths
VIDEO_DIRECTORY = "videos"
CSV_FILE = "video_metadata.csv"
JSON_FILE="ActualJsonFile.json"


# Maximum number of times to retry before giving up.
MAX_RETRIES = 5
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]
VALID_PRIVACY_STATUSES = ('public', 'private', 'unlisted')
