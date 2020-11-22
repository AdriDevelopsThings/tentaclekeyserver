from flask import request

from resources import app
from resources.paths.get import get
from resources.paths.upload import upload


@app.route("/pks/lookup")
def pks_lookup():
    return get("ascii_armored")


@app.route("/pks/add")
def pks_add():
    return upload(request.form["keytext"])
