import csv
import json
from config import JSON_FILE
CSV_FILE = "hello.csv"
OUTPUT_JSON = JSON_FILE


def convertCsvToJson():
    videos = []

    with open(CSV_FILE, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            video = {}

            for key, value in row.items():
                if value is None:
                    video[key] = None
                    continue

                value = value.strip()

                # Convert Tags → List
                if key.lower() == "tags":
                    video[key] = [tag.strip() for tag in value.split(",") if tag.strip()]

                # Convert boolean fields
                elif value.lower() in ["true", "false"]:
                    video[key] = value.lower() == "true"

                # Keep everything else as string
                else:
                    video[key] = value

            videos.append(video)

    # Save JSON
    with open(OUTPUT_JSON, "w", encoding="utf-8") as json_file:
        json.dump(videos, json_file, indent=4, ensure_ascii=False)

    print("✅ JSON file created successfully:", OUTPUT_JSON)
    return videos


import json
from datetime import datetime

def load_videos_from_json(file_path=JSON_FILE):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

if __name__ == "__main__":
    convertCsvToJson()
