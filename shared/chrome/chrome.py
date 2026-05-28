import os
import sys
import socket
from selenium import webdriver
import winreg #chromeのパスを取得用
import subprocess
from selenium.webdriver.chrome.options import Options
import logging

def create_driver(port, user_data_dir):
    """
    作成したクロームのseleniumドライバーを返す
    """
    if not is_browser_running(port):
        launch_chrome(port, user_data_dir)

    try:
        driver = webdriver.Chrome(options=set_options(port, user_data_dir))
    except Exception as e:
        logging.exception("Chrome接続失敗")
        sys.exit(1)

    driver.execute_script("""
    Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
    })
    """)

    return driver

def set_options(port, user_data_dir):
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

    return options

def launch_chrome(port, user_data_dir):
    """
    find_chromeで見つけたchrome.exeを開く
    """
    chrome_exe = find_chrome()

    if not chrome_exe:
        raise Exception("Chromeが見つかりませんでした。")

    subprocess.Popen([chrome_exe, f'--remote-debugging-port={port}', f'--user-data-dir={user_data_dir}'])

def is_browser_running(port):
    """
    指定したポートが使用中（ブラウザが起動中）か確認する
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # 接続できればポートが開いている（＝ブラウザが起動している）
        return s.connect_ex(('127.0.0.1', port)) == 0

def find_chrome():
    """
    プログラムを稼働する端末上でgoogle chromeのパスを探す関数
    パスが見つかればchrome.exeのパスを返す
    見つからなければNoneを返す
    """
    # 1. レジストリから探す (Windows)
    try:
        reg_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path) as key:
            return winreg.QueryValue(key, None)
    except Exception:
        pass

    # 2. 環境変数から探す
    path = shutil.which("chrome")
    if path: return path

    # 3. 一般的なデフォルトパスを直接確認
    default_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    ]
    for p in default_paths:
        if os.path.exists(p): return p

    return None
