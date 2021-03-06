import gnupg
from flask import Flask
from flask_limiter import Limiter

from resources.config import SQLALCHEMY_PATH, GPG_HOME_DIR
from resources.remote_addr import get_remote_address

app = Flask(__name__)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["400 per day", "100 per hour"]
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_PATH
gpg = gnupg.GPG(gnupghome=GPG_HOME_DIR)


def load():
    from resources.database import db, create_all
    from resources.database import key, keyserver, key_keyserver_association, uid, key_uid_association

    create_all()
    from resources.paths import get
    from resources.paths import index
    from resources.paths import get_by_fingerprint
    from resources.paths import upload
    from resources.paths import default_keyserver


loaded = False
if not loaded:
    loaded = True
    load()
