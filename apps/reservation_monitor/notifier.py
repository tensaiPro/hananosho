import logging
import json
import requests
from datetime import datetime


def send_line_message(

        message,

        token,

        group_id

):


    headers = {

        "Authorization":

        f"Bearer {token}"

    }


    payload = {

        "to":

        group_id,

        "messages":[

            {

                "type":"text",

                "text":

                message

            }

        ]

    }


    r=requests.post(

        "https://api.line.me/v2/bot/message/push",

        headers=headers,

        json=payload,

        timeout=10

    )


    r.raise_for_status()



def notify(

        queue,

        token,

        group_id,

        max_count=5

):


    now=datetime.now()


    if not (

        6<=now.hour<22

    ):

        return queue


    targets=queue[:max_count]


    if not targets:

        return queue


    msg=[

        "【予約通知】",

        f"件数:{len(targets)}"

    ]


    for item in targets:

        msg.append(

            f"{item['予約番号']}\n"

            f"{item['予約区分']}\n"

            f"{item['チェックイン日']}"

        )


    send_line_message(

        "\n".join(msg),

        token,

        group_id

    )


    logging.info(

        "通知完了"

    )


    return queue[max_count:]
