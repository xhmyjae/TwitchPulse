import json
import csv

with open("data/chat_messages_mynthos.json", "r") as f:
    data = json.load(f)

with open("data/chat_messages_chat_messages_mynthos.csv", "w", newline='', encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["username", "content", "timestamp"])
    writer.writeheader()
    for row in data:
        writer.writerow(row)
