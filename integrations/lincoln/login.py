from shared.config.loader import load_yml_config
import os
from pathlib import Path
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
import logging
import time

BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "configs" / "lincoln.yml"
_config = load_yml_config(CONFIG_PATH)

LOGIN_TITLE = _config["tl_lincoln"]["html_login_title"]
LOGIN_URL = _config["tl_lincoln"]["login_url"]
TOPPAGE_URL = _config["tl_lincoln"]["top_page_url"]
FORCE_LOGIN_TOPPAGE_URL = _config["tl_lincoln"]["force_login_toppage_url"]
RESERVATION_URL = _config["tl_lincoln"]["reservation_url"]

def login_lincoln(driver, user_id, pw) :
    retry_count = 0
    MAX_RETRY = 10

    while retry_count < MAX_RETRY:
        retry_count += 1
        if retry_count == MAX_RETRY:
            raise WebDriverException(f"{MAX_RETRY}回ログインを試みましたが失敗しました。 サーバーメンテ、パスワード変更などの可能性があります。")
        time.sleep(2)
        timeout_ok_button = driver.find_elements(By.ID, "extensionButton")
        if len(timeout_ok_button) and timeout_ok_button[0].is_displayed():
            timeout_ok_button[0].click()
            try:
                re_login_ok_button = WebDriverWait(driver, 5).until(
                    EC.visibility_of_element_located((By.ID, "failureButton"))
                )
                re_login_ok_button.click()

            except Exception as e:
                logging.info("タイムアウト後、ログイン状態は保持された状態のため、再ログインはしませんでした。")

        session_timeout = driver.find_elements(By.ID, "moveButton")
        if len(session_timeout) and session_timeout[0].is_displayed():
            session_timeout[0].click()

        if LOGIN_URL in driver.current_url:
            if driver.title == LOGIN_TITLE:
                usrid_txtbox = driver.find_element(By.ID, "txt_usrId")
                pw_txtbox = driver.find_element(By.ID, "password")
                usrid_txtbox.clear()
                pw_txtbox.clear()
                usrid_txtbox.send_keys(user_id)
                pw_txtbox.send_keys(pw)
                driver.find_element(By.ID, "doLogin").click()
                WebDriverWait(driver, 10).until(
                    EC.url_changes(LOGIN_URL)
                )
                time.sleep(2) #2秒待機

        elif TOPPAGE_URL in driver.current_url or FORCE_LOGIN_TOPPAGE_URL in driver.current_url:
            try:
                force_login_button = WebDriverWait(driver, 5).until(
                EC.visibility_of_all_elements_located((By.ID, "doForceLogout"))
                )
                if len(force_login_button):
                    force_login_button[0].click()
                    time.sleep(2)
            except Exception as e:
                logging.info("強制ログインなしでログインしました。")
            return True

        else:
            driver.get(LOGIN_URL)
