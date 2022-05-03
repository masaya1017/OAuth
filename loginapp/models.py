# __init__.pyに定義されているものをここでは呼び出す。
from loginapp import db, login_manager
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import UserMixin
import string
import random

# ログイン時に、ユーザIDを指定してデータを取得する。


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# モデルクラスの作成
class User(UserMixin, db.Model):
    # テーブル名の定義
    __tablename__ = 'users'
    # カラム定義(ユーザID/名前に対して、一つのEメールしか登録できない)
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), index=True, unique=True, nullable=True)
    username = db.Column(db.String(64))
    password = db.Column(db.String(128))
    # コンストラクタみたいなものでインスタンス化時でデータがセットされる。

    def __init__(self, email, username=None, password=None):
        self.email = email
        self.username = username
        if password is None:
            letters = string.ascii_lowercase
            password = ''.join(random.choice(letters) for _ in range(10))
        # 暗号化のために、パスワードはハッシュ化する。
        self.password = generate_password_hash(password)

    # emailはユニークなので必ず一件しか取得できない。
    @ classmethod
    def select_by_email(cls, email):
        return cls.query.filter(cls.email == email).first()
    # user情報をセットする。
    # dbにおいて、一旦セッションとして追加し、問題なければコミットする。

    def add_user(self):
        db.session.add(self)
        db.session.commit()
