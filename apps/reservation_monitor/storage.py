from shared.storage.json_read_write import load_json, save_json

import json
import os
import logging

QUEUE_DIR = "storage"

NOTIFY_QUEUE_FILE = os.path.join(
    QUEUE_DIR,
    "notify_queue.json"
)

SENT_QUEUE_FILE = os.path.join(
    QUEUE_DIR,
    "sent_queue.json"
)


def load_queue(path):

    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    except FileNotFoundError:
        return []

    except json.JSONDecodeError:
        logging.exception(f"{path} JSON破損")
        return []


def save_queue(path, data):

    os.makedirs(QUEUE_DIR, exist_ok=True)

    tmp = path + ".tmp"

    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

    os.replace(tmp, path)


def update_notification_queue(new_reservations):

    queue = load_queue(NOTIFY_QUEUE_FILE)

    for reservation in new_reservations:

        queue.append({
            "status": reservation.status,
            "reserve_no": reservation.reserve_no,
            "checkin": reservation.checkin,
            "raw": reservation.raw,
        })

    save_queue(NOTIFY_QUEUE_FILE, queue)

    logging.info(
        f"通知キュー追加件数: {len(new_reservations)}"
    )
