import requests
from bs4 import BeautifulSoup
import re
import sys
import chardet

# ページ宣言と旅館名の定義
page = 0   # ループ最初で加算するのでここでは0
hotel_name = "由布院ことぶき花の庄"
loop_num = 0   # ループ回数を格納する

# 花の庄が見つかった場合この変数にTrueを代入
found = False

# 花の庄が見つかるまでループ
while not found:

  # 詳細不明だが、じゃらんnetはPV数か何かで掲載順位がやたら変動する時があるようでページ遷移後に花の庄が前のページに
  # 移っていることがあるみたいなので見つからなかった場合もう一度最初から
  if(page >= 8):
    page = 0
    loop_num += 1

  # 見つからなければ次のページでループ再開
  page += 1

  # じゃらんの湯布院・湯平エリアのロード
  load_url = "https://www.jalan.net/440000/LRG_440600/SML_440602/page" + str(page) + ".html"
  response = requests.get(load_url)
  soup = BeautifulSoup(response.content, "lxml")   # 何故かlxmlでパースしてsoupオブジェクトを取得すると全て読み込まないので仕方なくhtml.parserを使う

  # 広告を削除
  ads = soup.select(".s16_00.fb")   # 広告のみにあるクラス二つを検索してそのタグをadsに格納
  [ad.decompose() for ad in ads]    # 広告をタグごと消去

  # じゃらんはh2タグのp-searchResultItem__facilityNameクラスが宿、その中のリンクを取得するためaタグを抽出
  # hotels = soup.select("h2.p-searchResultItem__facilityName > a")
  # いつの間にかh2.p-searchResultItem__facilityNameだけで良くなってたみたい 2023/2/23
  hotels = soup.select("h2.p-searchResultItem__facilityName")
  # 数えるための変数を1で初期化
  count = 1

  # print(hotels) # for debug
  # ページ内の旅館に花の庄があるか検索
  for hotel in hotels:
    # 花の庄を探す
    # print(hotel.text)
    if(hotel.text.startswith(hotel_name)):   # 花の庄の旅館名の後ろにスペースがあるようなので前方一致で検索
      found = True   # ループの終了
      break
    count += 1

  # found = True   # remove first hash key on this row for debug

  # ３回ループして見つからなければ強制終了
  if(loop_num >= 3):
    sys.exit("花の庄が見つかりませんでした。")
    break

ranking = str(30 * (page - 1) + count)
mes = "じゃらんnetで " + hotel_name + "は現在、" + str(page) + "ページ目の" + str(count) + "番目に掲載されています"
print(mes)
print("全体で " + ranking + "番目")
