import os
import time
import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert


CSV_PATTERN_NAME = "料理ランク取得用"


def download_reservation_csv(driver):

    current_handles = driver.window_handles

    logging.info("CSV出力開始")

    # ----------------------------------
    # CSV出力画面
    # ----------------------------------
    driver.execute_script(
        "doCsvOut();"
    )

    WebDriverWait(driver, 10).until(
        lambda d: len(d.window_handles)
        > len(current_handles)
    )

    new_handle = list(
        set(driver.window_handles)
        - set(current_handles)
    )[0]

    driver.switch_to.window(new_handle)

    # ----------------------------------
    # 出力パターン選択
    # ----------------------------------
    #カスタマイズした項目を出力のラジオボタンをクリック
    WebDriverWait(driver,10).until(
        EC.invisibility_of_element_located(
            (By.ID,"_BlockPanel")
        )
    )
    target_text = "カスタマイズした項目を出力"
    custom_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, f"//span[text()='{target_text}']")
            )
        )
    custom_button.click()
    #セレクトボックスで料理ランク取得用を選択
    WebDriverWait(driver,10).until(
        EC.invisibility_of_element_located(
            (By.ID,"_BlockPanel")
        )
    )
    select_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (
                By.NAME,
                "outCustomPtnId"
            )
        )
    )

    select_box = Select(select_element)

    found = False

    for option in select_box.options:

        if option.text.strip() == CSV_PATTERN_NAME:

            select_box.select_by_visible_text(
                CSV_PATTERN_NAME
            )

            found = True
            break

    if not found:

        raise RuntimeError(
            f"{CSV_PATTERN_NAME} が見つかりません"
        )

    logging.info("料理ランク取得用を選択")

    # ----------------------------------
    # 出力実行
    # ----------------------------------
    driver.execute_script("doOutput();")
    Alert(driver).accept()

    logging.info("CSV出力実行")

    time.sleep(5)

    driver.close()

    driver.switch_to.window(
        driver.window_handles[0]
    )
