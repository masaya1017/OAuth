sql_DBを作成したい方
*すでに作成済みの
![image](https://user-images.githubusercontent.com/82097439/166395917-cb44080d-ab7d-45d2-bb7a-c2503d45432f.png)



migrationsフォルダとdata.sqliteを削除する。
そのうえで以下を実行する。
➀working_directoryに移動
➁SET FLASK_APP=app.py(linuxだとSETではなく、EXPORT）をターミナル上で実行
➂flask db init⇒DBの初期化
➃flask db migrate -m "initial migrate"⇒マイグレーションによるDBの作成
➄flask db upgrade⇒DBのアップグレード

上記を実行すると、
![image](https://user-images.githubusercontent.com/82097439/166395822-dcf03bee-a763-4cac-b265-482888691d3d.png)



のように[data.sqlite]が作成される。


