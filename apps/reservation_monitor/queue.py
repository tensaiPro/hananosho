import json
import os
import logging

from shared.date import is_within_n_days

QUEUE_DIR = "storage"

NOTIFY_QUEUE_FILE = os.path.join(
    QUEUE_DIR,
    "notify_queue.json"
)

SENT_QUEUE_FILE = os.path.join(
    QUEUE_DIR,
    "sent_queue.json"
)

WITHIN_DAYS = 7


# --------------------------------------------------
# JSONロード
# --------------------------------------------------
def load_queue(path):

    try:

        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    except FileNotFoundError:

        return []

    except json.JSONDecodeError:

        logging.exception(f"{path} JSON破損")
        return []


# --------------------------------------------------
# JSON保存
# --------------------------------------------------
def save_queue(path, data):

    os.makedirs(QUEUE_DIR, exist_ok=True)

    tmp = path + ".tmp"

    with open(tmp, "w", encoding="utf-8") as f:

        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2
        )

    os.replace(tmp, path)


# --------------------------------------------------
# 通知キュー更新
# --------------------------------------------------
def update_notification_queue(new_reservations):

    # 通知待ちキュー
    notify_queue = load_queue(
        NOTIFY_QUEUE_FILE
    )

    # 通知済みキュー
    sent_queue = load_queue(
        SENT_QUEUE_FILE
    )

    # 通知済み検索高速化
    sent_map = {
        item.get("予約番号"): item
        for item in sent_queue
    }

    added_count = 0

    # 古い順で処理
    for reservation in reversed(new_reservations):

        reserve_no = reservation.reserve_no
        status = reservation.status
        checkin = reservation.checkin

        # N日以内判定
        is_within = is_within_n_days(
            checkin,
            WITHIN_DAYS
        )

        # 通知済み存在判定
        already_sent = reserve_no in sent_map

        # --------------------------------------------------
        # 新規予約
        # --------------------------------------------------
        if status == "予約":

            # N日以内だけ通知
            if not is_within:

                logging.info(
                    f"{reserve_no} 新規だがN日外"
                )

                continue

            logging.info(
                f"{reserve_no} 新規予約追加"
            )

            notify_queue.append(
                reservation.raw
            )

            added_count += 1

        # --------------------------------------------------
        # 変更
        # --------------------------------------------------
        elif status == "変更":

            # 通知済みなら
            # 宿泊日変更の可能性あるので通知
            if already_sent:

                logging.info(
                    f"{reserve_no} 変更通知"
                )

                notify_queue.append(
                    reservation.raw
                )

                added_count += 1

            else:

                # 未通知ならN日以内だけ
                if is_within:

                    logging.info(
                        f"{reserve_no} 未通知変更追加"
                    )

                    notify_queue.append(
                        reservation.raw
                    )

                    added_count += 1

        # --------------------------------------------------
        # 取消
        # --------------------------------------------------
        elif status == "取消":

            logging.info(
                f"{reserve_no} 取消通知"
            )

            notify_queue.append(
                reservation.raw
            )

            added_count += 1

        else:

            logging.info(
                f"{reserve_no} 未知ステータス"
            )

    save_queue(
        NOTIFY_QUEUE_FILE,
        notify_queue
    )

    logging.info(
        f"通知キュー追加件数: {added_count}"
    )
