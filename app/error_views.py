from flask import render_template, request
from app import app


@app.errorhandler(404)
def page_not_found(e):
    app.logger.warning("404 Error: %s", request.path)
    return render_template("404.html"), 404
