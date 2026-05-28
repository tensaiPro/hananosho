from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import time
import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta
from typing import Optional

def search_reservations(
    driver,
    noticed_search_from: Optional[datetime] = None,  #受信日で検索する場合の開始日
    noticed_search_to: Optional[datetime] = None,    #受信日で検索する場合の終了日
    check_in_search_from: Optional[datetime] = None, #チェックイン日で検索する場合の開始日
    check_in_search_to: Optional[datetime] = None,   #チェックイン日で検索する場合の終了日
    search_with_noticed=True,   #受信日で検索する場合True ※search_with_check_inがTrueでも衝突しない
    search_with_check_in=False, #チェックイン日で検索する場合True
    sort_key="sendDt", #検索結果のソート    デフォルトで受信時間順
    sort_order="2"     #検索結果のソート順  デフォルトで降順
):
    """
    予約検索実行

    Args:
        search_from : 何日から検索するか
        search_to : 何日まで検索するか
        search_with
    """

    noticed_search_from = (noticed_search_from or datetime.now() + relativedelta(days=-1))

    noticed_search_to = (noticed_search_to or datetime.now())

    check_in_search_from = (check_in_search_from or datetime.now())

    check_in_search_to = (check_in_search_to or datetime.now())

    # ローディング終了待ち
    WebDriverWait(driver,10).until(
        EC.invisibility_of_element_located(
            (By.ID,"_BlockPanel")
        )
    )

    #検索条件をクリア
    #まず受信日とチェックイン日以外の検索条件をクリア
    driver.execute_script("doClear('0');")
    WebDriverWait(driver,10).until(
        EC.invisibility_of_element_located(
            (By.ID,"_BlockPanel")
        )
    )
    #受信日とチェックイン日はdoClear('0')してもクリアされないので日付未入力のラジオボタンでクリア
    target_text = "日付未入力"
    search_date_clear_buttons = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, f"//span[text()='{target_text}']")
            )
        )

    for clear_button in search_date_clear_buttons:
        WebDriverWait(driver,10).until(
            EC.invisibility_of_element_located(
                (By.ID,"_BlockPanel")
            )
        )
        clear_button.click()

    #全てのセレクトボックスが表示されるまで待つ
    WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.TAG_NAME, "select"))
    )


    # 検索条件選択
    #受信日設定
    if search_with_noticed:
        _set_data_range(driver, "notice", noticed_search_from, noticed_search_to)

    #チェックイン日設定
    if search_with_check_in:
        _set_data_range(driver, "checkIn", check_in_search_from, check_in_search_to)

    time.sleep(1)

    # 検索実行
    driver.execute_script("doSearch('0');")

    WebDriverWait(driver,10).until(
        EC.invisibility_of_element_located(
            (By.ID,"_BlockPanel")
        )
    )

    # 受信日時降順ソート
    old_table = driver.find_element(By.ID, "resultTableBody")

    driver.execute_script(f"doSort('{sort_key}', '{sort_order}')")

    WebDriverWait(driver,10).until(EC.staleness_of(old_table))


    logging.info(f"検索完了")

def _set_data_range(driver, prefix, from_date, to_date):
    """
    受信日、もしくはチェックイン日で条件を設定する
    prefixで受け取った文字列'checkIn'(チェックイン日)もしくは'notice'(受信日)の検索範囲を設定する
    範囲が31日以上になると検索できないのでその場合は30日に修正する
    """
    if from_date > to_date:
        from_date, to_date = to_date, from_date
        logging.info(f"prefix{prefix}の検索条件がfrom_date > to_dateだったので値を入れ替えました。")
    if (to_date - from_date).days >= 31:
        to_date = from_date + relativedelta(days=30)
        logging.info("受信日の検索範囲が30日を超えていたので範囲を開始日から30日に修正しました。")
    Select(driver.find_element(By.NAME, f"{prefix}FromYear")).select_by_value(str(from_date.year))
    Select(driver.find_element(By.NAME, f"{prefix}FromMonth")).select_by_value(f"{from_date.month:02}")
    Select(driver.find_element(By.NAME, f"{prefix}FromDay")).select_by_value(f"{from_date.day:02}")
    Select(driver.find_element(By.NAME, f"{prefix}ToYear")).select_by_value(str(to_date.year))
    Select(driver.find_element(By.NAME, f"{prefix}ToMonth")).select_by_value(f"{to_date.month:02}")
    Select(driver.find_element(By.NAME, f"{prefix}ToDay")).select_by_value(f"{to_date.day:02}")
