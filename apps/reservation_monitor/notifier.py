import logging

from .queue import (
    load_queue,
    save_queue,
    NOTIFY_QUEUE_FILE,
    SENT_QUEUE_FILE,
)


# --------------------------------------------------
# 通知処理
# --------------------------------------------------
def notify():

    notify_queue = load_queue(
        NOTIFY_QUEUE_FILE
    )

    if not notify_queue:

        logging.info(
            "通知対象なし"
        )

        return

    sent_queue = load_queue(
        SENT_QUEUE_FILE
    )

    for item in notify_queue:

        reserve_no = item.get(
            "予約番号",
            ""
        )

        status = item.get(
            "予約区分",
            ""
        )

        logging.info(
            f"通知: "
            f"{reserve_no} "
            f"{status}"
        )

        # 本来ここでLINE通知

        # 通知済みに移動
        sent_queue.append(item)

    # 通知済み保存
    save_queue(
        SENT_QUEUE_FILE,
        sent_queue
    )

    # 通知待ち削除
    save_queue(
        NOTIFY_QUEUE_FILE,
        []
    )

    logging.info(
        "通知完了"
    )
