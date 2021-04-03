import os
import datetime
import json
import re
from my_module import kanji, setup

def load_data():
	# 今日時点のデータがまだダウンロードされていない場合ダウンロードする
	today = datetime.date.today().strftime("%Y-%m-%d")
	if (not os.path.exists("data/japanese-addresses-cities_" + today + ".json")):
		setup.download_latest_data()

	# ダウンロード済みJSONを読み込む	
	json_prefs = json.load(open("data/japanese-addresses-prefs_" + today + ".json"))
	json_cities = json.load(open("data/japanese-addresses-cities_" + today + ".json"))

	return (json_prefs, json_cities)

def trim_whitespace(string):
	whitespaces = str.maketrans({
		'\u3000': '',
		' ': '',
		'\t': ''
	})
	return string.translate(whitespaces)


class AddressNormalizer:
	def __init__(self):
		self.prefs, self.cities = load_data()

	def normalize(self, address):
		address = trim_whitespace(address)

		# 都道府県名の正規化
		prefecture = ""
		for pref in self.prefs:
			_pref = re.sub("(都|道|府|県)$", "", pref)
			regexp = re.compile(_pref + '(都|道|府|県)')
			if (re.match(regexp, address) != None):
				prefecture = pref
				address = address[len(pref):]
				break

		if (prefecture == ""):
			raise NormalizationError("Can't detect the prefecture.", address)

		# 市区町村名の正規化
		city = ""
		# 少ない文字数の地名に対してミスマッチしないように文字の長さ順にソート
		cities = self.cities[prefecture]
		cities.sort(reverse=True, key=len)

		address = trim_whitespace(address)
		for _city in cities:
			if (re.match(kanji.normalize(_city), kanji.normalize(address)) != None):
				city = _city
				address = address[len(city):]
				break
			else:
				# 以下 `xxx郡` が省略されているケースに対する対応
				if (0 < address.find("郡")):
					# `郡山市` のように `郡` で始まる地名はスキップ(address.find("郡")が0)
					__city = re.sub(".+郡", "", _city)
					if (0 == kanji.normalize(address).find(kanji.normalize(__city))):
						city = _city
						address = address[len(city):]
						break
		
		if (city == ""):
			raise NormalizationError("Can't detect the city.", address)

		# 180行目まで翻訳した
		# https://github.com/geolonia/normalize-japanese-addresses/blob/2b679f9673d27fd98f4c8a9a5a39d407d23778e3/src/main.ts#L108

		return {
			"pref": prefecture,
			"city": city,
			"town": "",
			"block": address
		}


class NormalizationError(Exception):
	pass

a = AddressNormalizer()
print(a.normalize("北海道札幌市西区24-2-2-3-3"))