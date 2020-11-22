from resources.database import db


class GPGKey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fingerprint = db.Column(db.String(40), nullable=False, unique=True)
    date = db.Column(db.DateTime, nullable=True)
    uids = db.relationship("GPGUid", secondary="key_uid_association", back_populates="keys")
    keyservers = db.relationship("GPGKeyServer", secondary="key_key_server_association", back_populates="keys")

    def __init__(self, fingerprint, date):
        self.fingerprint = fingerprint
        self.date = date
