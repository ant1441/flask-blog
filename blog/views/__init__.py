import time
import logging
from flask import g
from blog import app

log = logging.getLogger(__name__)


@app.before_request
def before_request():
    # For page generation timing
    g.request_start_time = time.time()
    g.request_time = lambda: "%.5fs" % (
        time.time() - g.request_start_time)
