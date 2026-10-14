import csv
import os
from datetime import datetime


def log_event(sender, message, reply, status):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    file_path = "data/chat_log.csv"
    os.makedirs("data", exist_ok=True)

    # Check: file new hai ya empty?
    file_exists = os.path.exists(file_path)
    is_empty = not file_exists or os.path.getsize(file_path) == 0
    try:
        with open(file_path, "a", newline="", encoding="utf-8") as file:
            columns = ["timestamp", "sender", "message", "reply", "status"]

            writer = csv.DictWriter(file, fieldnames=columns)

            # Header sirf first time likho
            if is_empty:
                writer.writeheader()

            # Har event ek nayi row mein
            writer.writerow({
                "timestamp": current_time,
                "sender": sender,
                "message": message,
                "reply": reply,
                "status": status
            })

    
    except PermissionError:
        print("CSV band karo, shayad Excel mein khuli hai. Phir dobara try karo.")