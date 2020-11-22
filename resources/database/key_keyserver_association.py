from resources.database import db


class KeyKeyServerAssociation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key_id = db.Column(db.Integer, db.ForeignKey("gpg_key.id"))
    keyserver_id = db.Column(db.Integer, db.ForeignKey("gpg_key_server.id"))
