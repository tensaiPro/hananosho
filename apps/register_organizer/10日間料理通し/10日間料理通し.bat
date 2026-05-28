//実行するコマンドを非表示
@echo off

//VBScriptを実行（第一引数：マクロファイルのフルパス　第二引数：マクロ名）
//カレントディレクトリ：%~dp0
xlsToXlsx.vbs %~dp0\xlsToXlsx.xlsm xlsToXlsx
python -u 10日間料理通し整理用.py
