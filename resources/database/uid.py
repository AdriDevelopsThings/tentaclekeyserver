from resources.database import db


class GPGUid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Text, nullable=False)
    keys = db.relationship("GPGKey", secondary="key_uid_association", back_populates="uids")

    def __init__(self, uid):
        self.uid = uid
