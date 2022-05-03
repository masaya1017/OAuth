<サーバの立ち上げ方>
git cloneやzipフォルダとしてローカルに落としておく。
その後、VScodeを開き、app.pyを開いて、実行すればよい。ターミナル上でサーバのURLのリンクが開くので、そこをクリックすればよい。

<sql_DBを作成したい方> \
*すでに作成済みの \
migrationsフォルダとdata.sqliteを削除する。\
そのうえで以下を実行する。\
➀working_directoryに移動 \
➁SET FLASK_APP=app.py(linuxだとSETではなく、EXPORT）をターミナル上で実行 \
➂flask db init⇒DBの初期化 \
➃flask db migrate -m "initial migrate"⇒マイグレーションによるDBの作成 \
➄flask db upgrade⇒DBのアップグレード 

上記を実行すると \
migrationsフォルダと[data.sqlite]が作成される。


