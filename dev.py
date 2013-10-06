#!/usr/bin/env python

if __name__ == "__main__":
    from blog import app
    app.run('0.0.0.0', debug=True)
