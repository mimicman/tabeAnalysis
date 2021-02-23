import requests
import csv
from bs4 import BeautifulSoup
import re
import matplotlib.pyplot as plt

root_url = 'https://tabelog.com/tokyo/' # 食べログURL
max_page = 60       # 最大表示ページ
url      = root_url # スクレイピングしていくURL
x        = []       # x軸 駅までの距離
y        = []       # y軸 評価

# 最大ページまで繰り返し
for page in range(2, max_page, 1):
    res      = requests.get(url)
    # HTMLパーサーでHTMLを扱いやすいようなデータに変換する
    soup     = BeautifulSoup(res.content, 'html.parser')
    # 駅からの距離を配列で取得
    distance = soup.find_all('div' , class_='list-rst__area-genre cpy-area-genre')
    rate     = soup.find_all('span', class_='c-rating__val c-rating__val--strong list-rst__rating-val')
    # スペースと"/"以降の文字を削除する（駅までの距離を取得）
    for (distance,rate) in zip(distance,rate):
        # 1つだけフォーマットが異なるデータがあったのでスキップする
        if '世田谷区' in re.sub('.*駅', '', re.sub('/[^/]*$', '', distance.text)).strip().replace('m', ''):
            continue
        # 距離の数字以外の文字を省いてx軸に加える
        x.append(int(re.sub('.*駅', '', re.sub('/[^/]*$', '', distance.text)).strip().replace('m', '')))
        # 評価をy軸に加える
        y.append(float(rate.text))
    # 次のページのURLを取得
    url = root_url + 'rstLst/RC/' + str(page) + '/'

# 散布図
plt.scatter(x, y)
# グラフの可視化
plt.show()