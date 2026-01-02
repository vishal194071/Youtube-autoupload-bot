import os
import logging
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

from config import (
    CLIENT_SECRETS_FILE,
    YOUTUBE_TOKEN_FILE,
    SHEET_TOKEN_FILE,
    YOUTUBE_UPLOAD_SCOPE,
    SHEET_AND_DRIVE_SCOPE,
    YOUTUBE_API_SERVICE_NAME,
    YOUTUBE_API_VERSION,
)

# ------------------------------------------------------------------
# Logging setup
# ------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)


def auth():
     youtube = YouTubeAuth.get_service()
     sheet=SheetAuth.get_service()

# ------------------------------------------------------------------
# Shared OAuth Logic
# ------------------------------------------------------------------
def _get_credentials(token_file, scopes):
    creds = None

    # Ensure token directory exists
    token_dir = os.path.dirname(token_file)
    if token_dir and not os.path.exists(token_dir):
        os.makedirs(token_dir, exist_ok=True)
        logger.info(f"📁 Created token directory: {token_dir}")

    # Load existing token
    if os.path.exists(token_file):
        logger.info(f"🔑 Loading token from {token_file}")
        creds = Credentials.from_authorized_user_file(token_file, scopes)

    # Refresh or authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            logger.info("♻️ Refreshing expired token...")
            creds.refresh(Request())
        else:
            logger.info("🔐 Starting OAuth flow...")
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE,
                scopes
            )
            creds = flow.run_local_server(port=0)

        with open(token_file, "w") as token:
            token.write(creds.to_json())
            logger.info(f"✅ Token saved at {token_file}")

    return creds


# ------------------------------------------------------------------
# YouTube Auth
# ------------------------------------------------------------------
class YouTubeAuth:
    @staticmethod
    def get_service():
        logger.info("🚀 Initializing YouTube API service...")

        creds = _get_credentials(
            token_file=YOUTUBE_TOKEN_FILE,
            scopes=YOUTUBE_UPLOAD_SCOPE
        )

        service = build(
            YOUTUBE_API_SERVICE_NAME,
            YOUTUBE_API_VERSION,
            credentials=creds
        )

        logger.info("✅ YouTube service initialized successfully")
        return service


# ------------------------------------------------------------------
# Google Sheets Auth
# ------------------------------------------------------------------
class SheetAuth:
    @staticmethod
    def get_service():
        logger.info("📊 Initializing Google Sheets API service...")

        creds = _get_credentials(
            token_file=SHEET_TOKEN_FILE,
            scopes=SHEET_AND_DRIVE_SCOPE
        )

        service = build("sheets", "v4", credentials=creds)

        logger.info("✅ Google Sheets service initialized successfully")
        return service
