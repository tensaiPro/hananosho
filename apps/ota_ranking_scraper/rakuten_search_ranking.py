import requests
from bs4 import BeautifulSoup
import re
 
# ページ宣言と旅館名の定義、リスティング広告URLに含まれる文字列の定義
page = 0   # ループ最初で加算するのでここでは0
hotel_name = "由布院温泉　由布院ことぶき　花の庄"
ads_ref = "id=hotelList_ad_"
 
# 花の庄が見つかった場合この変数にTrueを代入
found = False
 
# 花の庄が見つかるまでループ 
while not found:
 
  # 見つからなければ次のページでループ再開
  page += 1
 
  # 楽天トラベルの湯布院・湯平エリアのロード
  load_url = "https://search.travel.rakuten.co.jp/ds/yado/oita/yufuin-p" + str(page)   # 楽天トラベルはURLの最後にページの番号
  res = requests.get(load_url)
  soup = BeautifulSoup(res.content, "lxml") 
 
  # h1タグの子要素のaタグの抽出(楽天トラベルは施設の名前をh1タグ内のaタグで表記)
  hotels = soup.select("h1 > a")
 
  # 数えるための変数を1で初期化
  count = 1
 
  for hotel in hotels:
    # リンクに広告URLのみに含まれる文字列があればスルー
    if(ads_ref in hotel.get("href")):
      continue
    
    # 花の庄が見つかった場合ループを脱出
    if(re.match(hotel.text, hotel_name)):
      found = True   # ループの終了
      break
 
    # 花の庄じゃない場合カウント+1
    count += 1
 
# 結果表示
ranking = str(30 * (page - 1) + count)
mes = "楽天トラベルで " + hotel_name + "は現在、" + str(page) + "ページ目の" + str(count) + "番目に掲載されています"
print(mes)
print("全体で " + ranking + "番目")
