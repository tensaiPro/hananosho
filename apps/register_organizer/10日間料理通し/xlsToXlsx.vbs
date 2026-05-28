//Excel操作を可能にする為のオブジェクトを作成
Dim obj
Set obj = WScript.CreateObject("Excel.Application")

//Excel処理を画面非表示
obj.Visible = false

//バッチファイルでこのファイルを実行する際の引数設定
//第一引数：指定したExcelマクロを開く
obj.Workbooks.Open WScript.Arguments(0)
//第二引数：指定したマクロを実行
obj.Application.Run WScript.Arguments(1)
