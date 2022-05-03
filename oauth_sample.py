import os
from flask_dance.contrib.google import make_google_blueprint, google
from flask import Flask, redirect, url_for

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

app = Flask(__name__)
app.secret_key = "supersekrit"  # Replace this with your own secret!
blueprint = make_google_blueprint(
    client_id="",
    client_secret="",
    scope=[
        "https://www.googleapis.com/auth/plus.me",
        "https://www.googleapis.com/auth/userinfo.email",
    ]
)
app.register_blueprint(blueprint, url_prefix="/login")


@app.route("/")
def index():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v2/userinfo")
    assert resp.ok, resp.text
    return "You are @{login} on Google".format(login=resp.json()["email"])


if __name__ == '__main__':
    # app.run(host='0.0.0.0',port=8000)
    app.run(debug=True, port=5000)
