import urllib.parse

import requests

from resources.config import (
    REDIRECT_KEY_SERVERS,
    REDIRECT_KEY_PATH,
    REDIRECT_KEY_ADD_PATH,
)


class GPGRawKey:
    def __init__(self, ascii_armored_key, fount_on_keyserver):
        self.ascii_armored_key = ascii_armored_key
        self.fount_on_keyserver = fount_on_keyserver


def get_key(qry) -> GPGRawKey:
    redirect_key_path = REDIRECT_KEY_PATH.replace(
        "{SEARCH_QUERY}", urllib.parse.quote(qry)
    )
    for keyserver in REDIRECT_KEY_SERVERS:
        print(f"GET {qry} from {keyserver}...")
        path = keyserver + redirect_key_path
        response = requests.get(path)
        if response.status_code == 404:
            continue
        response.raise_for_status()
        return GPGRawKey(response.text, keyserver)


def upload_key(key: GPGRawKey, key_servers=REDIRECT_KEY_SERVERS):
    k = []
    for keyserver in key_servers:
        if key.fount_on_keyserver != keyserver:
            print(f"POST to {keyserver}")
            response = requests.post(
                keyserver + REDIRECT_KEY_ADD_PATH,
                data={"keytext": key.ascii_armored_key},
            )
            response.raise_for_status()
            k.append(keyserver)
    return k
