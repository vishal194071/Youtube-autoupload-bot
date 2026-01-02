# uploader.py

import time
import random
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
from config import VIDEO_CATEGORY, PRIVACY_STATUS


class VideoUploader:

    def __init__(self, youtube):
        self.youtube = youtube

    def upload(self, file_path, title, description, tags, publish_time):
        body = {
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags,
                "categoryId": VIDEO_CATEGORY,
                "defaultLanguage": "en",
            },
            "status": {
                "privacyStatus": PRIVACY_STATUS,
                "publishAt": publish_time.isoformat() + "Z",
            },
        }

        media = MediaFileUpload(file_path, chunksize=-1, resumable=True)

        request = self.youtube.videos().insert(
            part="snippet,status",
            body=body,
            media_body=media
        )

        self._resumable_upload(request)

    def _resumable_upload(self, request):
        response = None
        retry = 0

        while response is None:
            try:
                print("⬆️ Uploading...")
                status, response = request.next_chunk()

                if response and "id" in response:
                    print(f"✅ Uploaded successfully: {response['id']}")
                    return

            except HttpError as e:
                if e.resp.status in [500, 502, 503, 504]:
                    print(f"⚠️ Retriable error: {e}")
                else:
                    raise

            except Exception as e:
                print(f"⚠️ Error: {e}")

            retry += 1
            if retry > 10:
                print("❌ Max retries reached.")
                return

            sleep_time = random.uniform(1, min(60, 2 ** retry))
            print(f"🔄 Retrying in {sleep_time:.2f}s")
            time.sleep(sleep_time)
