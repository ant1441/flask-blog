#!/usr/bin/env python
from werkzeug.contrib.profiler import ProfilerMiddleware
from app import app

if __name__ == '__main__':
    app.config['PROFIE'] = True
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[30])
    app.run()
