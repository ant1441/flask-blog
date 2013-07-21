#!/usr/bin/env python
import os


if __name__ == "__main__":
    os.environ['LOG_CFG'] = "production.yaml"
    from blog import app
    app.run()
