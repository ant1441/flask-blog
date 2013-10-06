#!/usr/bin/env python
from os.path import join
from setuptools import setup

for line in open(join('blog', '__init__.py')):
    if '__version__' in line:
        version = eval(line.split('=')[-1])
        break
else:
    raise AssertionError('__version__ = "VERSION" must be in __init__.py')

setup(
    name="blog",
    version=version,
    description="Simple blogging software.",
    author="Adam Hodgen",
    author_email="ant1441@gmail.com",
    packages=["blog"],
    install_requires=['Flask==0.9',
                      'Flask-SQLAlchemy==0.16',
                      'Flask-Login',
                      'Flask-WTF==0.8.3',
                      'Flask-Admin',
                      'PyYaml',
                      'markdown',
                      'psycopg2',
                      ],
    include_package_data=True,
)
