#!/usr/bin/env python
from werkzeug.contrib.profiler import ProfilerMiddleware

if __name__ == '__main__':
    from blog import app
    os.environ['LOG_CFG'] = "production.yaml"
    app.config['PROFIE'] = True
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[30])
    app.run()
