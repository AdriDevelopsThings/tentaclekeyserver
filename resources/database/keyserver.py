from resources.database import db


class GPGKeyServer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text, nullable=False)
    keys = db.relationship("GPGKey", secondary="key_key_server_association", back_populates="keyservers")

    def __init__(self, url):
        self.url = url
