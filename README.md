# weather
アメダスの情報を簡易に仕入れることを目的としたクローラ  
`http://www.jma.go.jp/`から拠点付近のアメダス情報を入手し,表形式で出力させるプログラム  
オフラインでも確認ができるよう,最新データをcsvに保存している  
  
本プログラムはpython3.Xでの実行を前提としてる  
また,beautifulsoup4とprettytableが必要 

## 導入
`$ git clone https://github.com/H4TM4N/weather.git`

## 使用方法


オンライン時: 
$ python online.py

オフライン時: 
$ python offline.py

# forecast
天気予報を簡易に表示することを目的としたクローラ  
`http://www.jma.go.jp/`から選択した地域の天気予報を取得し表示するプログラム  
引数になんでもいいので追加すれば地域選択から実行  
引数が指定されなければ直近の選択地域の天気予報を表示する  
  
## 使用方法
  
地域選択:  
$ python forecast.py a
  
天気予報表示:  
$ python forecast.py
