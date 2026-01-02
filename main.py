# main.py

import os
from auth import YouTubeAuth
from uploader import VideoUploader
from csvJson import load_videos_from_json
from config import VIDEO_DIRECTORY, CSV_FILE
import json


def main():
    youtube = YouTubeAuth.get_service()
    uploader = VideoUploader(youtube)
    filepath="exampleJsonFile.json"
    videosMetadata = load_videos_from_json(file_path=filepath)
    for videoMetadata in videosMetadata:
        print(videoMetadata)
        print("\n")
        print("\n")
        print("-------------------")
        uploader.uploadVideoAndThumbnail(videoMetadata)

if __name__ == "__main__":
    main()
