# scheduler.py

import datetime
import csv
import os
from config import SET_SIZE, START_DATE, SCHEDULE_TIMINGS, VIDEO_DIRECTORY


class VideoScheduler:

    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.videos = self._load_csv()

    def _load_csv(self):
        if not os.path.exists(self.csv_file):
            raise FileNotFoundError("CSV file not found")

        with open(self.csv_file, encoding="utf-8") as f:
            return list(csv.DictReader(f))

    def get_batches(self):
        start_date = datetime.datetime.strptime(START_DATE, "%Y-%m-%d")

        for i in range(0, len(self.videos), SET_SIZE):
            publish_date = start_date + datetime.timedelta(days=i // SET_SIZE)
            batch = self.videos[i:i + SET_SIZE]
            yield publish_date, batch

    def get_publish_time(self, publish_date, index):
        hour, minute = SCHEDULE_TIMINGS[index]
        return publish_date.replace(hour=hour, minute=minute, second=0)
