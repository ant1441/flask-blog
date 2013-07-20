#!/usr/bin/env python
import os


os.environ['LOG_CFG'] = "development.yaml"
if __name__ == "__main__":
    from blog import app
    app.run()
