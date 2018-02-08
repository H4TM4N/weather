# weather
アメダスの情報を簡易に仕入れることを目的としたクローラ  
`http://www.jma.go.jp/`から拠点付近のアメダス情報を入手し,表形式で出力させるプログラム  
オフラインでも確認ができるよう,最新データをcsvに保存している

## 導入
`$ git clone https://github.com/H4TM4N/weather.git`

## 使用方法
本プログラムはpython3.Xでの実行を前提としてる  
また,beautifulsoup4とprettytableを用いるので環境が必要  

オンライン時: 
$ python online.py

オフライン時: 
$ python offline.py
