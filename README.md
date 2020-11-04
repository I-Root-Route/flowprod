# サイトURL
https://flowprod.herokuapp.com

# 注意点
Webスクレイピングでデータを取得する先のサイトや、YouTube、Spotifyの不具合によって表示されない場合があります。  
YouTubeのAPIコール(100回/日)を超えると正しく表示されません  

# 使用技術
フロントエンド: HTML/CSS
Webフレームワーク: Flask(Python)
ライブラリ: Spotify API, YouTube API, Beautiful Soup, etc.  
デプロイ: Heroku  

# 機能 使用法
ホーム画面の検索窓にアーティスト名を入れるとそのアーティストの楽曲に関する情報が自動生成されます。  
主に海外EDM, POPアーティスト名を入れる事が想定されるため、その他のジャンルのアーティスト名を入れた場合は結果に空欄がある場合があります。
