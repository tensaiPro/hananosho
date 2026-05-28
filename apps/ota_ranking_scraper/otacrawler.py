class Otacrawler:
    def __init__(self):
        self.ranking = 0
        self.facnum = 0
        self.cheepest = ""
        self.useads = []
        self.adsnum = 0

    def crawl(self):
        return

class Rakuten(Otacrawler):
    def crawl(self):
        import requests
        from bs4 import BeautifulSoup
        import re

        # ページ宣言と旅館名の定義、リスティング広告URLに含まれる文字列の定義
        page = 0   # ループ最初で加算するのでここでは0
        hotel_name = "由布院温泉　由布院ことぶき　花の庄"
        ads_ref = "id=hotelList_ad_"
        ads_num = 0

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
                if page == 1:
                    ads_num += 1
                    self.useads.append(hotel.text)
                continue

            # 花の庄が見つかった場合ループを脱出
            if(re.match(hotel.text, hotel_name)):
              found = True   # ループの終了
            if found and page != 1:
                break
            # 花の庄じゃない場合カウント+1
            count += 1

          if page == 1:
              self.facnum = count
        # 結果表示
        self.ranking = (page - 1) * self.facnum + count
