# auth.py

import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

from config import (
    CLIENT_SECRETS_FILE,
    TOKEN_FILE,
    YOUTUBE_UPLOAD_SCOPE,
    YOUTUBE_API_SERVICE_NAME,
    YOUTUBE_API_VERSION
)

class YouTubeAuth:
    @staticmethod
    def get_service():
        creds = None

        if os.path.exists(TOKEN_FILE):
            creds = Credentials.from_authorized_user_file(
                TOKEN_FILE, YOUTUBE_UPLOAD_SCOPE
            )

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CLIENT_SECRETS_FILE,
                    YOUTUBE_UPLOAD_SCOPE
                )
                creds = flow.run_local_server(port=0)

            with open(TOKEN_FILE, "w") as token:
                token.write(creds.to_json())

        return build(
            YOUTUBE_API_SERVICE_NAME,
            YOUTUBE_API_VERSION,
            credentials=creds
        )
