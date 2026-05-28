import logging
from datetime import datetime,timedelta


def is_within_n_days(
        date_str,
        n_days
):

    if not date_str:
        return False


    try:

        date_clean = (
            date_str
            .split()[0]
            [:10]
        )

        target = datetime.strptime(

            date_clean,
            "%Y.%m.%d"

        ).date()

        today = datetime.today().date()

        return (

            today <= target <=

            today +
            timedelta(
                days=n_days
            )

        )

    except:

        return False



def update_queue(
        queue,
        reservations,
        within_days
):

    idx_map = {

        item["予約番号"]:i

        for i,item

        in enumerate(queue)

    }


    for r in reversed(reservations):

        res_id = r.reserve_no

        valid = (

            is_within_n_days(

                r.checkin,
                within_days

            )

        )


        idx = idx_map.get(
            res_id
        )


        if idx is not None:

            if (

                r.status=="取消"

                or

                not valid

            ):

                queue.pop(idx)

            else:

                queue[idx]=r.raw


        else:

            if (

                valid

                and

                r.status in [

                    "予約",
                    "変更"

                ]

            ):

                queue.insert(

                    0,
                    r.raw

                )



    return queue
