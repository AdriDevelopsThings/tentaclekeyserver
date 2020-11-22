from resources.database import db


class KeyUidAssociation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key_id = db.Column(db.Integer, db.ForeignKey("gpg_key.id"))
    uid_id = db.Column(db.Integer, db.ForeignKey("gpg_uid.id"))
