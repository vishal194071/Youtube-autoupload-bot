# main.py

from auth import auth,YouTubeAuth,SheetAuth
from uploader import VideoUploader
from csvJson import load_videos_from_json
from config import JSON_FILE
from sheets import SpreadSheet
import json



def main():
    auth()
    uploader = VideoUploader(YouTubeAuth.get_service())
    spreadSheet=SpreadSheet(SheetAuth.get_service())
    videosMetadatas=spreadSheet.videosToUpload()
    for videoMetadata in videosMetadatas:
        print(f"uploading {videoMetadata}\n\n \n")
        uploader.uploadVideoAndThumbnail(videoMetadata)
        print("Done")

if __name__ == "__main__":
    main()
