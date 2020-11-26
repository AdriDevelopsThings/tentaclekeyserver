from flask import render_template, Response

from resources import app
from resources.config import MY_DOMAIN, GOOGLE_ANALYTICS_GTAG


@app.route("/")
def index():
    return render_template("index.html", gtag=GOOGLE_ANALYTICS_GTAG)


@app.route("/robots.txt")
def robots_txt():
    return Response(
        f"""# robots.txt for {MY_DOMAIN}

User-agent: *
Allow: *
    """,
        mimetype="text/plain",
    )
