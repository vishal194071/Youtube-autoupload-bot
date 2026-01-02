import os
import time
import random
import httplib2
import http.client as httplib

from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

from auth import YouTubeAuth

# Retry config
MAX_RETRIES = 10
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

httplib2.RETRIES = 1

RETRIABLE_EXCEPTIONS = (
    httplib2.HttpLib2Error,
    IOError,
    httplib.NotConnected,
    httplib.IncompleteRead,
    httplib.ImproperConnectionState,
    httplib.CannotSendRequest,
    httplib.CannotSendHeader,
    httplib.ResponseNotReady,
    httplib.BadStatusLine,
)


class VideoUploader:
    def __init__(self, youtube):
        self.youtube = youtube

    # ---------------- UPLOAD VIDEO ---------------- #
    def read(self,video_id="JvaBYNjhi3c"):
        response = self.youtube.videos().list(
        part="snippet,status,recordingDetails,localizations",
            id=video_id
        ).execute()

        print(f"response: {response}")

    def upload(self, metadata):
        # self.read()
        # return
        print(f"Uploading video with info: {metadata}")
        body = {
            "snippet": {
                "title": metadata["title"],
                "description": metadata["description"],
                "tags": metadata.get("tags", []),
                "categoryId": metadata["categoryId"],
                "defaultLanguage": metadata["defaultLanguage"],
                "localized": {
                            "title": metadata["title"],
                            "description": metadata["description"],
                            },
                "defaultAudioLanguage": metadata["defaultAudioLanguage"],

            },
            "status": {
                "privacyStatus": metadata["privacyStatus"],
                "madeForKids": metadata["madeForKids"]
            },
            "recordingDetails": {
                "locationDescription":metadata["locationDescription"],
                "location": {
                "latitude": metadata["latitude"],
                "longitude": metadata["longitude"],
                "altitude": metadata["altitude"]
                },
                "recordingDate": metadata["recordingDate"]
            },
            "localizations": {
                                "en-IN": {
                                "title":  metadata["title"],
                                "description":  metadata["description"],
                                }
                            }


        }

        request = self.youtube.videos().insert(
            part="snippet,status,recordingDetails,localizations",
            body=body,
            media_body=MediaFileUpload(
                metadata["file"],
                chunksize=-1,
                resumable=True
            )
        )

        return self._resumable_upload(request)

    # ---------------- UPDATE METADATA ---------------- #
    def update_video(self, video_id, title=None, description=None, tags=None):
        response = self.youtube.videos().list(part="snippet",id=video_id).execute()

        if not response["items"]:
            raise Exception("Video not found")

        snippet = response["items"][0]["snippet"]

        if title:
            snippet["title"] = title

        if description:
            snippet["description"] = description

        if tags:
            snippet["tags"] = tags

        self.youtube.videos().update(
            part="snippet",
            body={
                "id": video_id,
                "snippet": snippet
            }
        ).execute()

        print("✅ Video metadata updated successfully")

    # ---------------- THUMBNAIL ---------------- #
    def upload_thumbnail(self, video_id, thumbnail_path):
        print("Uploading Thumbnail....")
        if not os.path.exists(thumbnail_path):
            raise FileNotFoundError("Thumbnail file not found")

        self.youtube.thumbnails().set(
            videoId=video_id,
            media_body=MediaFileUpload(thumbnail_path)
        ).execute()

        print("✅ Thumbnail uploaded successfully.")

    # ---------------- RESUMABLE UPLOAD ---------------- #
    def _resumable_upload(self, request):
        response = None
        error = None
        retry = 0

        while response is None:
            try:
                print("Uploading video...")
                status, response = request.next_chunk()

                if response and "id" in response:
                    print(f"✅ Video uploaded: {response['id']}")
                    return response["id"]

            except HttpError as e:
                if e.resp.status in RETRIABLE_STATUS_CODES:
                    error = f"Retriable HTTP error {e.resp.status}: {e.content}"
                else:
                    raise

            except RETRIABLE_EXCEPTIONS as e:
                error = f"Retriable error: {e}"

            if error:
                retry += 1
                if retry > MAX_RETRIES:
                    raise Exception("❌ Max retries exceeded")

                sleep_time = random.uniform(1, 2 ** retry)
                print(f"{error}\nRetrying in {sleep_time:.2f}s...")
                time.sleep(sleep_time)


    def uploadVideoAndThumbnail(self,metadata):
        try:
            video_id=self.upload(metadata=metadata)
            thumbnail_path= metadata["thumbnail"]
            self.upload_thumbnail(video_id, thumbnail_path)
        except HttpError as e:
            print(f"❌ HTTP Error {e.resp.status}: {e.content}")


# ================= MAIN ================= #
if __name__ == "__main__":
    youtube =  YouTubeAuth.get_service()
    uploader = VideoUploader(youtube)

    try:
        # uploader.update_video_metadata(id)
        uploader.read(id)

    except HttpError as e:
        print(f"❌ HTTP Error {e.resp.status}: {e.content}")
