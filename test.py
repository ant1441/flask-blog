#!/usr/bin/env python
import os
from app import app 
import unittest
from coverage import coverage
import sys

cov = coverage(branch=True, omit=['test.py', '*/.virtualenvs/*'])
cov.start()

class blogTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_index(self):
        indx = self.app.get("/")
        assert "Adam's Blog" in indx.data

    def test_docType(self):
        indx = self.app.get("/")
        assert "<!DOCTYPE html>" in indx.data

if __name__ == "__main__":
    try:
        unittest.main()
    except SystemExit as sysexit:
        if sysexit.args[0] is True:
            raise
    except:
        e = sys.exc_info()[0]
        print("Exception: ", e)

    cov.stop()
    cov.save()
    print("\n\nCoverage Report:\n")
    cov.report()
    #print("HTML version: ", os.path.join(basedir, "tmp/coverage/index.html"))
    cov.html_report(directory = "tmp/coverage")
    cov.erase()
