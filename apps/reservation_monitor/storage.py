import json
import os
import logging


STATE_DIR = "storage"

STATE_FILE = os.path.join(
    STATE_DIR,
    "reservation_state.json"
)

MAX_SAVE_COUNT = 10


# --------------------------------------------------
# storageディレクトリ作成
# --------------------------------------------------
def ensure_storage_dir():

    os.makedirs(
        STATE_DIR,
        exist_ok=True
    )


# --------------------------------------------------
# state読み込み
# --------------------------------------------------
def load_state():

    ensure_storage_dir()

    try:

        with open(
            STATE_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except FileNotFoundError:

        logging.info(
            "stateファイルなし"
        )

        return []

    except json.JSONDecodeError:

        logging.exception(
            "state JSON破損"
        )

        return []


# --------------------------------------------------
# state更新
# --------------------------------------------------
def update_state(current_reservations):

    ensure_storage_dir()

    save_data = []

    # 最新10件保存
    for reservation in current_reservations[:MAX_SAVE_COUNT]:

        save_data.append(
            reservation.raw
        )

    tmp = STATE_FILE + ".tmp"

    with open(
        tmp,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            save_data,
            f,
            ensure_ascii=False,
            indent=2
        )

    os.replace(
        tmp,
        STATE_FILE
    )

    logging.info(
        f"state保存件数: {len(save_data)}"
    )
