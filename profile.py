#!/usr/bin/env python
from werkzeug.contrib.profiler import ProfilerMiddleware
from blog import app

if __name__ == '__main__':
    app.config['PROFIE'] = True
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[30])
    app.run()
