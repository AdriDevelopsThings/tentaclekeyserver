REDIRECT_KEY_SERVERS = ["https://keyserver.ubuntu.com", "http://keys.gnupg.net"]
REDIRECT_KEY_PATH = "/pks/lookup?search={SEARCH_QUERY}&fingerprint=on&hash=on&exact=on&options=mr&op=get"
REDIRECT_KEY_ADD_PATH = "/pks/add"
SQLALCHEMY_PATH = "mysql+pymysql://root@localhost/test"
MY_DOMAIN = "http://example.test"
GPG_HOME_DIR = ".gnupg"
GOOGLE_ANALYTICS_GTAG = None
X_FORWARDED_HEADER_FIELD = None  # string or None for disable
CLOUDFLARE = False
