import os
import logging
import portalocker

from integrations.lincoln.parser import row_to_reservation
from integrations.lincoln.models import Reservation
from pathlib import Path
from shared.config.loader import load_yml_config
from shared.logger.logger import setup_logging
from shared.chrome.chrome import create_driver
from integrations.lincoln.login import login_lincoln
from integrations.lincoln.navigation import move_to_reservation
from integrations.lincoln.scraper import fetch_reservations
from integrations.lincoln.search import search_reservations
from integrations.lincoln.csv_parser import parse_reservation_csv
from integrations.lincoln.csv_export import download_reservation_csv
from .storage import load_state, update_state
from .compare import detect_new_reservations
from .queue import update_notification_queue
from .notifier import notify
from .set_chrome_options import set_chrome_options

# -------------------------------
# 外部ファイルのパス設定
# -------------------------------

BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "config" / "lincoln.yml"
LOG_DIR = BASE_DIR / "logs"

# -------------------------------
# main関数定義
# -------------------------------
def main():

    PROGRAM_NAME = os.path.basename(__file__)
    config = load_yml_config(CONFIG_PATH)
    logging.info("=" * 50)
    logging.info(f"{PROGRAM_NAME} 起動しました。")


    DEBUG = config["general"]["debug_mode"] #デバッグモードか本番か設定

    # -------------------------------
    # LINE通知設定
    # -------------------------------
    LINE_CHANNEL_ACCESS_TOKEN = config["line"]["channel_access_token"]
    LINE_GROUP_ID = config["line"]["group_id"]

    #chromeをseleniumドライバを取得
    port = config["chrome"]["chrome_port"]
    user_data_dir = config["chrome"]["user_data_dir"]

    driver = create_driver(port, user_data_dir, set_chrome_options(port, user_data_dir))


    #ログイン処理～予約業務ページに行くまでループ
    LOGIN_ID = config["tl_lincoln"]["login_id"]
    LOGIN_PW = config["tl_lincoln"]["login_pw"]

    login_lincoln(driver, LOGIN_ID, LOGIN_PW)

    move_to_reservation(driver)

    search_reservations(driver)

    current_reservations = fetch_reservations(driver)

    saved_state = load_state()

    new_reservations = detect_new_reservations(current_reservations, saved_state)

    if new_reservations:
        download_reservation_csv(driver)

        csv_rows = parse_reservation_csv()

        logging.info(
            f"CSV件数:{len(csv_rows)}"
        )

    update_state(current_reservations)

    update_notification_queue(new_reservations)

    #notify()

# -------------------------------
# プログラムの多重起動阻止
# -------------------------------
LOCK_FILE = f"{os.path.splitext(os.path.basename(__file__))[0]}.lock"

if __name__ == "__main__":
    try:
        # -------------------------------
        # logging設定
        # -------------------------------
        setup_logging(LOG_DIR)
        with portalocker.Lock(LOCK_FILE, timeout=0):
            # -------------------------------
            # main関数呼び出し
            # -------------------------------
            main()

    except portalocker.exceptions.LockException:
        logging.info("多重起動を検知したため終了")
        sys.exit(0)
