#!/usr/bin/env python
from werkzeug.contrib.profiler import ProfilerMiddleware
from app import app

app.config['PROFIE'] = True
app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions = [30])
app.run(debug=True)
