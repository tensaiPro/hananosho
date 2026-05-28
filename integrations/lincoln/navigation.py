from shared.config.loader import load_yml_config
import os
import sys
from pathlib import Path
import logging
from selenium.webdriver.support.ui import WebDriverWait

BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "configs" / "lincoln.yml"
_config = load_yml_config(CONFIG_PATH)
MAX_RETRY = 5
RESERVATION_URL = _config["tl_lincoln"]["reservation_url"]

def move_to_reservation(driver):
    """
    ログイン後のリンカーンから予約業務ページに移動する
    """
    driver.get(RESERVATION_URL)
    WebDriverWait(driver,10).until(
        lambda d:
            RESERVATION_URL in d.current_url
    )
    logging.info("予約業務画面に移動しました。")
