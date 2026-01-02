# main.py

from auth import auth,YouTubeAuth
from uploader import VideoUploader
from csvJson import load_videos_from_json
from config import JSON_FILE

def main():
    auth()
    uploader = VideoUploader(YouTubeAuth.get_service())

    # videosMetadata = load_videos_from_json(file_path=JSON_FILE)
    # for videoMetadata in videosMetadata:
    #     uploader.uploadVideoAndThumbnail(videoMetadata)

if __name__ == "__main__":
    main()
