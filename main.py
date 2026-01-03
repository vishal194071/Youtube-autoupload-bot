# main.py

from auth import auth,YouTubeAuth,SheetAuth
from uploader import VideoUploader
from sheets import SpreadSheet
import json



def process_tags(tags):
    if not tags:
        return []
    
    # support both | and , as separators
    if "|" in tags:
        return [t.strip() for t in tags.split("|") if t.strip()]
    else:
        return [t.strip() for t in tags.split(",") if t.strip()]

def main():
    auth()
    uploader = VideoUploader(YouTubeAuth.get_service())
    spreadSheet=SpreadSheet(SheetAuth.get_service())
    videosMetadatas=spreadSheet.videosToUpload()
    for videoMetadata in videosMetadatas:
        videoMetadata["tags"] = process_tags(videoMetadata["tags"])
        print(f"uploading {videoMetadata}\n\n \n")
        uploader.uploadVideoAndThumbnail(videoMetadata)
        print("Done")

if __name__ == "__main__":
    main()
