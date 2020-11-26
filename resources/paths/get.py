from werkzeug.exceptions import BadRequest, NotFound

from resources import app, limiter
from flask import request, Response, render_template

from resources.domain_logic import download_key
from resources.utils import add_fingerprint_spaces


@app.route("/get")
@limiter.limit("100/hour")
@limiter.limit("400/day")
def get(output="pretty"):
    raw_search = request.args.get("search", None)
    search = ""
    for s in raw_search:
        if s != " " or len(search) > 0:
            search += s
    while search.endswith(" "):
        search = search[:len(search) - 1]
    if not search:
        raise BadRequest(
            description=BadRequest.description + " Please add the 'search' get field."
        )
    auto_upload = (
        True
        if request.args.get("auto_upload", "true").lower() in ("true", "1", "yes", "on")
        else False
    )
    force_loading = (
        True
        if request.args.get("force_loading", "false").lower()
        in ("true", "1", "yes", "on")
        else False
    )
    output = request.args.get("output", output).lower()
    if output not in ("pretty", "ascii_armored", "json"):
        raise BadRequest(
            description=BadRequest.description
            + "The 'output' field must contain 'pretty', 'ascii_armored' or "
            "'json'."
        )
    j, db_keys = download_key(
        search, auto_upload=auto_upload, force_loading=force_loading
    )
    if not j:
        raise NotFound()
    if output == "pretty":
        return render_template(
            "show.html",
            s_qry=search,
            keys=db_keys,
            upload=j["upload"],
            uri=f"/get?search=S_QRY&output={output}&auto_upload={auto_upload}&force_loading={force_loading}",
            add_fingerprint_spaces=add_fingerprint_spaces
        )
    elif output == "ascii_armored":
        return Response(j["key"], mimetype="text/plain")
    elif output == "json":
        return j
