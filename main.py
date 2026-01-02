# main.py

import os
from auth import YouTubeAuth
from uploader import VideoUploader
from scheduler import VideoScheduler
from config import VIDEO_DIRECTORY, CSV_FILE


def main():
    youtube = YouTubeAuth.get_service()
    uploader = VideoUploader(youtube)
    scheduler = VideoScheduler(CSV_FILE)

    for batch_index, (publish_date, batch) in enumerate(scheduler.get_batches(), start=1):
        print(f"\n📅 Batch {batch_index} → {publish_date.date()}")

        for idx, row in enumerate(batch):
            file_name = row["File_name"].strip()
            file_path = os.path.join(VIDEO_DIRECTORY, file_name)

            if not os.path.exists(file_path):
                print(f"⚠️ File missing: {file_name}")
                continue

            publish_time = scheduler.get_publish_time(publish_date, idx)

            print(f"🚀 Scheduling {file_name} at {publish_time} UTC")

            uploader.upload(
                file_path=file_path,
                title=row["title"].strip(),
                description=row["description"].strip(),
                tags=[t.strip() for t in row["tags"].split(",")],
                publish_time=publish_time
            )


if __name__ == "__main__":
    main()
