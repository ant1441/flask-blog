from flask import render_template, request
from blog import app


@app.errorhandler(404)
def page_not_found(e):
    app.logger.warning("404 Error: %s from %s",
                       request.path,
                       request.remote_addr)
    return render_template("error/404.html"), 404

app.errorhandler(500)
def server_error(e):
    app.logger.warning("500 Error: %s from %s",
                       request.path,
                       request.remote_addr)
    return render_template("error/500.html"), 500
