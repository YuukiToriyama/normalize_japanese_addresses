import requests
import datetime
import json

# Geolonia住所データAPIにアクセス
# 最新の住所データをダウンロード
endpoint = 'https://geolonia.github.io/japanese-addresses/api/ja'

def download_latest_data():
    response = requests.get(endpoint + ".json")
    if (response.status_code == 200):
    	cities = response.json()
    	prefs = list(cities.keys())

    	# キャッシュを作成するために今日の日付を取得
    	today = datetime.date.today().strftime("%Y-%m-%d")

    	# 都道府県リスト 及び 全国の自治体名リスト をdata/に保存
    	with open("./data/japanese-addresses-prefs_" + today + ".json", "w") as file:
    		json.dump(prefs, file, ensure_ascii=False)
    	with open("./data/japanese-addresses-cities_" + today + ".json", "w") as file:
    		json.dump(cities, file, ensure_ascii=False)