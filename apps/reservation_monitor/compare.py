import logging


def reservation_key(res):

    return (

        res.status,
        res.reserve_no,
        res.receive_dt,

    )


def detect_new_reservations(
        current,
        previous
):

    previous_keys = {

        (
            item.get("予約区分"),
            item.get("予約番号"),
            item.get("受信日時")

        )

        for item in previous

    }


    new_items = []

    for r in current:

        key = reservation_key(r)

        if key in previous_keys:

            continue

        new_items.append(r)


    logging.info(

        f"新規/変更検知:{len(new_items)}"

    )

    return new_items
