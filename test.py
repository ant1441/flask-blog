#!/usr/bin/env python
import os
from app import app 
import unittest
#import tempfile

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
    unittest.main()
