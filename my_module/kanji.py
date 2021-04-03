import csv

# JIS 第2水準 => 第1水準 及び 旧字体 => 新字体 の変換テーブルを読み込む
kanji_table = list(csv.reader(open('my_module/kanji.csv')))

# 大字の削除 及び 表記のゆれの削除
dict = {
    "大字": '',
    "ー": '一',
    "二": '二',
    "ハ": '八',
    "ヶ": 'が',
    "ケ": 'が',
    "之": 'の',
    "ノ": 'の',
    "ヵ": 'か',
    "カ": 'か',
    "ッ": 'つ',
    "ツ": 'つ'
}

def normalize(string):
	for key in dict:
		string = string.replace(key, dict[key])

	for pair in kanji_table:
		string = string.replace(pair[0], pair[1])

	return string