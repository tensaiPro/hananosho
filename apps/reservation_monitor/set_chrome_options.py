from selenium.webdriver.chrome.options import Options
import os

def set_chrome_options(port, user_data_dir):
    """
    スクレイピング用のseleniumドライバーにオプションを設定
    """
    #webdriverが検知されると毎回2FAしないといけないので検知されないように設定
    options = Options()
    options.add_argument(f"--user-data-dir={user_data_dir}")
    options.add_experimental_option("debuggerAddress", f"127.0.0.1:{port}") #同じブラウザを使うためのポート指定、デバッグモード
    #options.add_experimental_option("detach", True) #プログラムを終了してもブラウザを閉じない
    options.add_argument(r'--profile-directory=selenium')
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-popup-blocking")

    return options
