from datetime import datetime

from sqlalchemy.orm.exc import NoResultFound
from werkzeug.exceptions import abort

from resources import gpg, database
from resources.config import REDIRECT_KEY_SERVERS
from resources.database.key import GPGKey
from resources.database.keyserver import GPGKeyServer
from resources.database.uid import GPGUid
from resources.keyserver import get_key, GPGRawKey, upload_key


def get_keyserver(url, do_commit=True):
    try:
        return GPGKeyServer.query.filter(GPGKeyServer.url == url).one()
    except:
        ks = GPGKeyServer(url)
        database.add(ks, do_commit=do_commit)
        return ks


def download_key(search, auto_upload=False, force_loading=False):
    commit = False
    keys = {}
    db_uids = {}
    db_keys = []
    uploaded_data = {}
    k_dates = {}

    def gpg_load():
        for key in gpg.list_keys():
            uids = []
            if "uid" in key and key["uid"] not in (None, ""):
                uids.append(key["uid"])
            uids.extend(key["uids"])
            uids = [uid for uid in uids]
            fount = False
            for uid in uids:
                if search.lower() in uid.lower():
                    keys[key["fingerprint"]] = uids
                    fount = True
                    break
            if "date" in key:
                k_dates[key["fingerprint"]] = datetime.fromtimestamp(int(key["date"]))
            if fount:
                for uid in uids:
                    if uid not in db_uids:
                        try:
                            db_uids[uid] = GPGUid.query.filter(GPGUid.uid == uid).one()
                        except NoResultFound:
                            db_uids[uid] = GPGUid(uid)
                            database.add(db_uids[uid], do_commit=False)
                            commit = True

    gpg_load()
    if len(keys) == 0 or force_loading:
        k = get_key(search)
        if not k:
            abort(404)
        f = gpg.import_keys(k.ascii_armored_key).fingerprints
        for fingerprint in f:
            uploaded_data[fingerprint] = k.fount_on_keyserver
    gpg_load()
    for fingerprint, uids in keys.items():
        if fingerprint not in db_keys:
            db_k_uids = []
            for uid in uids:
                db_k_uids.append(db_uids[uid])
            try:
                db_k = GPGKey.query.filter(GPGKey.fingerprint == fingerprint).one()
            except NoResultFound:
                db_k = GPGKey(fingerprint, k_dates.get(fingerprint, None))
                db_k.uids = db_k_uids
                commit = True
            if db_k.uids != db_k_uids:
                db_k.uids = db_k_uids
                commit = True
            if (
                fingerprint in uploaded_data
                and get_keyserver(uploaded_data[fingerprint]) not in db_k.keyservers
            ):
                db_k.keyservers.append(get_keyserver(uploaded_data[fingerprint]))
                commit = True

            db_keys.append(db_k)
    j = {
        "key": gpg.export_keys([k.fingerprint for k in db_keys]),
        "fingerprints": [k.fingerprint for k in db_keys],
    }
    if auto_upload:
        u_keys = []
        u_keyserver = []
        for key in db_keys:
            ks = [
                item
                for item in REDIRECT_KEY_SERVERS
                if item not in [kss.url for kss in key.keyservers]
            ]
            if len(ks) > 0:
                u_keys.append(key.fingerprint)
            for o_ks in ks:
                if o_ks not in u_keyserver:
                    u_keyserver.append(o_ks)
        o = gpg.export_keys(u_keys)
        j["upload"] = upload_key(GPGRawKey(o, None), key_servers=u_keyserver)
        for key in db_keys:
            for ks in u_keyserver:
                d_ks = get_keyserver(ks)
                if d_ks not in key.keyservers:
                    key.keyservers.append(d_ks)
                    commit = True

    if commit:
        database.commit()
    return j, db_keys
