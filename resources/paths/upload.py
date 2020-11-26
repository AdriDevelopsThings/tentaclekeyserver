from datetime import datetime

from flask import request, redirect
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.exceptions import BadRequest

from resources import app, gpg, database, limiter
from resources.database.key import GPGKey
from resources.database.uid import GPGUid
from resources.domain_logic import get_keyserver
from resources.keyserver import upload_key, GPGRawKey

@limiter.limit("50/hour")
@limiter.limit("200/day")
@app.route("/upload", methods=["GET", "POST"])
def upload(key=None):
    if request.method != "POST":
        return redirect("/")
    if "key" not in request.values:
        raise BadRequest(BadRequest.description + " Please add the 'key' post field.")
    key = request.values.get("key", key)
    auto_upload = (
        True
        if request.values.get("auto_upload", "true").lower() in ("true", "1", "yes", "on")
        else False
    )
    output = request.values.get("output", "pretty").lower()
    if output not in ("pretty", "json"):
        raise BadRequest(
            description=BadRequest.description
                        + "The 'output' field must contain 'pretty' or "
                          "'json'."
        )
    fingerprints = gpg.import_keys(key).fingerprints
    keys = {}
    d_keys = {}
    for k in gpg.list_keys():
        for f in fingerprints:
            if f not in k and k["fingerprint"] == f:
                keys[f] = k
    del fingerprints
    for fingerprint, key in keys.items():
        uids = []
        d_uids = []
        if "uid" in key and key["uid"] not in (None, ""):
            uids.append(key["uid"])
        uids.extend(key["uids"])
        for uid in uids:
            try:
                d_uids.append(GPGUid.query.filter(GPGUid.uid == uid).one())
            except NoResultFound:
                gpg_uid = GPGUid(uid)
                database.add(gpg_uid, do_commit=False)
                d_uids.append(gpg_uid)
        try:
            d_key = GPGKey.query.filter(GPGKey.fingerprint == fingerprint).one()
        except NoResultFound:
            d_key = GPGKey(fingerprint, datetime.fromtimestamp(int(key["date"])))
            database.add(d_key, do_commit=False)
        d_key.uids = d_uids
        database.commit()
        d_keys[fingerprint] = d_key
    uploaded_ks = []
    if auto_upload:
        o = gpg.export_keys(list(keys.keys()))
        uploaded_ks = upload_key(GPGRawKey(o, None))
        d_uploaded_ks = []
        for uks in uploaded_ks:
            d_uploaded_ks.append(get_keyserver(uks, do_commit=False))
        for key in d_keys.values():
            key.keyservers = d_uploaded_ks
        database.commit()
    if output == "pretty":
        return f"""
        <html>
        <head>
        <title>Uploaded key(s)</title>
        </head>
        <body>
        <p>These fingerprints has been uploaded: {", ".join(keys.keys())} .</p>
        <p>The keys has been uploaded to these keyservers: {", ".join(uploaded_ks)} .</p>
        </body>
        </html>
        """
    elif output == "json":
        return {
            "status": "success",
            "uploaded_keyservers": uploaded_ks
        }



