from flask_dance.contrib.google import make_google_blueprint
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, redirect
import os
from uuid import uuid4


os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

login_manager = LoginManager()
login_manager.login_message = 'ログインしてください'

basedir = os.path.abspath(os.path.dirname(__name__))

# sqlalchemyと呼ばれるDB使用する。
db = SQLAlchemy()
migrate = Migrate()
# blueprintを使用する。
google_blueprint = make_google_blueprint(
    client_id="",
    client_secret="",
    scope=[
        "https://www.googleapis.com/auth/plus.me",
        "https://www.googleapis.com/auth/userinfo.email",
    ],
    # 認証後にリダイレクト(遷移策はviews.pyの[/google_login]となる。)
    redirect_to='app.google_login'
)
# __init__.pyで使用する[create_app]関数を作成する。


def create_app():
    app = Flask(__name__)
    # uuid4によって乱数をsecret_keyにセット
    # secret_keyはセッションなどのログイン情報に使用
    # configは初期設定を意味する
    app.config['SECRET_KEY'] = str(uuid4())
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'sqlite:///'+os.path.join(basedir, 'data.sqlite')
    app.config['SQLALCHEMY_TRACK_MODIFICATION'] = True
    # blueprintによって、ルート情報を登録することができる。
    app.register_blueprint(google_blueprint, url_prefix="/login")
    from loginapp.views import bp
    app.register_blueprint(bp)
    # dbの初期化を行い、マイグレーションを実行する。
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    return app
