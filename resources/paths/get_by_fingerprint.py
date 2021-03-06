from flask import Response, abort

from resources import app, gpg, limiter


@limiter.limit("100/hour")
@limiter.limit("200/day")
@app.route("/get/<string:fingerprint>")
def get_by_fingerprint(fingerprint):
    fingerprint = fingerprint.replace(" ", "")
    l_k = gpg.list_keys()
    for k in l_k:
        if k["fingerprint"] == fingerprint:
            return Response(gpg.export_keys([k["fingerprint"]]), mimetype="text/plain")
    abort(404)
