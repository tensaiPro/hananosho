from datetime import datetime, timedelta
import logging


# --------------------------------------------------
# 今日からN日以内判定
# --------------------------------------------------
def is_within_n_days(
    date_str,
    n_days
):

    if not date_str:

        return False

    try:

        # 2026.07.23(木)
        date_raw = date_str.split()[0]

        # YYYY.MM.DD
        date_clean = date_raw[:10]

        target_date = datetime.strptime(
            date_clean,
            "%Y.%m.%d"
        ).date()

        today = datetime.today().date()

        limit_date = today + timedelta(
            days=n_days
        )

        return (
            today <= target_date <= limit_date
        )

    except Exception:

        logging.exception(
            f"日付変換失敗: {date_str}"
        )

        return False
