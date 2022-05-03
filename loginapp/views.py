from flask import Blueprint, flash, request, render_template, redirect, url_for
from flask_login import login_user, login_required, logout_user
from loginapp.models import User
from flask_dance.contrib.google import google
from loginapp import google_blueprint

bp = Blueprint('app', __name__, url_prefix='')

# ルーティング(設定されているエンドポイントにアクセスしたら、htmlを返す。)


@bp.route('/')
def home():
    return render_template('home.html')


@bp.route('/google_login')
def google_login():
    # 認証がされていないときは、googleのログイン画面へリダイレクトさせる。
    if not google.authorized:
        return redirect(url_for("google.login"))
    # ログインされたとき
    resp = google.get("/oauth2/v2/userinfo")  # 認証情報を取得する。
    # 検証(レスポンスとデータの内容)
    assert resp.ok, resp.text
    # データの内容を確認
    print(resp)
    email = resp.json()["email"]
    # email情報より、DBに問い合わせる。
    user = User.select_by_email(email)
    # ユーザが登録されていないときは、とりあえず、emailのみを登録する。
    if not user:
        user = User(email=email)
        user.add_user()
    # ユーザ情報をログインマネージャーに記憶させる。
    login_user(user, remember=True)
    return render_template(
        'welcome.html', email=email
    )


@bp.route('/user')
@login_required
def user():
    return render_template('user.html')


@bp.route('/logout')
@login_required
def logout():
    if google.authorized:
        token = google_blueprint.token['access_token']
        resp = google.post(
            "https://accounts.google.com/o/oauth2/revoke",
            params={"token": token},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        assert resp.ok, resp.text
        del google_blueprint.token  # トークンの削除
    logout_user()
    return redirect(url_for('app.home'))
