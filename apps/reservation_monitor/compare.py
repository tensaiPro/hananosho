import logging


# --------------------------------------------------
# 比較キー
# --------------------------------------------------
COMPARE_KEYS = [

    "予約番号",
    "予約区分",
    "受信日時",
]


# --------------------------------------------------
# 比較用tuple生成
# --------------------------------------------------
def build_compare_key(raw):

    return tuple(
        raw.get(k, "")
        for k in COMPARE_KEYS
    )


# --------------------------------------------------
# 新規・変更・取消検知
# --------------------------------------------------
def detect_new_reservations(
    current_reservations,
    saved_state
):

    # 過去履歴キー集合
    saved_keys = set()

    for item in saved_state:

        saved_keys.add(
            build_compare_key(item)
        )

    new_reservations = []

    # 上から順番にチェック
    for reservation in current_reservations:

        key = build_compare_key(
            reservation.raw
        )

        # 一致したらそこで終了
        if key in saved_keys:

            break

        new_reservations.append(
            reservation
        )

    logging.info(
        f"新規検知件数: "
        f"{len(new_reservations)}"
    )

    # 古い順に並び替え
    return list(
        reversed(new_reservations)
    )
