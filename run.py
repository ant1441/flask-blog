#!/usr/bin/env python
import os


os.environ['LOG_CFG'] = "production.yaml"
if __name__ == "__main__":
    from blog import app
    app.run()
