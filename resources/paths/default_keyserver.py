from flask import request

from resources import app, limiter
from resources.paths.get import get
from resources.paths.upload import upload


@limiter.limit("100/hour")
@limiter.limit("400/day")
@app.route("/pks/lookup")
def pks_lookup():
    return get("ascii_armored")


@limiter.limit("50/hour")
@limiter.limit("200/day")
@app.route("/pks/add")
def pks_add():
    return upload(request.form["keytext"])
