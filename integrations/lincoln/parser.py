from .models import Reservation


def row_to_reservation(row: dict):

    return Reservation(

        reserve_no = row.get("予約番号", ""),

        status = row.get("予約区分", ""),

        receive_dt = row.get("受信日時", ""),

        checkin = row.get("チェックイン日", ""),

        checkout = row.get("チェックアウト日"),

        food_rank = row.get("料理ランク"),

        guests = row.get("人数"),

        reserve_type = row.get("予約種別"),

        raw=row
    )
