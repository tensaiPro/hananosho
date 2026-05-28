from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver

from integrations.lincoln.config import config
from integrations.lincoln.parser import row_to_reservation
from integrations.lincoln.models import Reservation


def fetch_reservations(driver) -> list[Reservation]:
    """
    リンカーン予約一覧テーブルを取得し
    Reservation オブジェクト一覧へ変換する
    """

    #不要なヘッダとスキップする列番号を_parse_headers関数で取得
    headers, skip_indices = _parse_headers(driver)

    #予約情報を行(tr)のリストでrowsに入れる
    rows = WebDriverWait(driver,10).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, '//tbody[@id="resultTableBody"]/tr')
        )
    )

    #戻り値であるReservationクラスを入れる空のリストを宣言
    reservations = []

    for row in rows:
        #row(tr)を_parse_rowに投げて不要なものを削除し、dict({"予約番号": "...", ...}) に変換したものをdataに入れる
        data = _parse_row(row, headers, skip_indices)
        #さらにrow_to_reservationに投げてrow→Reservationクラスに変換
        reservation = row_to_reservation(data)
        reservations.append(reservation)

    return reservations

def _get_skip_indices(headers):
    pass

def _parse_headers(driver):
    """
    ヘッダ解析
    Returns:
        headers #不要なヘッダを除外した実際に使用するヘッダ名のリスト
        skip_indices #テーブルの不要な列番号の集合
    """
    #不要なヘッダの集合をskip_headersにlincoln.ymlからロード
    skip_headers = set(config["reservation"]["skip_headers"])

    thead = WebDriverWait(driver,10).until(
        EC.presence_of_element_located(
            (By.XPATH,'//table[@id="resultTable"]/thead')
        )
    )
    #テーブルのヘッダの行(th)をリストでthsに格納
    ths = thead.find_elements(By.TAG_NAME,"th")
    #
    headers = []
    skip_indices = set()

    td_index = 0

    for th in ths:
        #ヘッダのthタグの中のテキストを取得
        text = th.text.strip()
        #thタグにcolspan属性が設定されていればint型にキャストしてcolspanに格納、設定がなければ1
        colspan = int(th.get_attribute("colspan") or 1)

        if text in skip_headers:
            #textがスキップする文字列であればskip_indicesにスキップする列番号を追加
            for i in range(colspan):
                skip_indices.add(td_index+i)
        else:
            #使用する文字列ならheadersに追加
            headers.append(text)

        td_index += colspan

    return headers, skip_indices

def _parse_row(row, headers, skip_indices) -> dict:
    """
    tr → dict変換
    """
    #予約のテーブルのボディのtdのリスト("選択"、"予約区分"、"チェックイン日"などに対応する値)をcolsに入れる
    cols = row.find_elements(By.TAG_NAME,"td")
    #戻り値で辞書型の空オブジェクトdataを宣言
    data = {}
    header_index = 0 # headers の現在位置

    for i,col in enumerate(cols):

        if i in skip_indices:
            continue
        #colsのデータをdata{"ヘッダ名":値}と変換していく
        data[headers[header_index]] = col.text.strip()

        header_index += 1

    return data
