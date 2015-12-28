#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from pip.req import parse_requirements

install_reqs = parse_requirements('requirements.txt')
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    # Clean existing build artifacts
    os.system('rm -rf dist')
    os.system('rm -rf build')
    os.system('rm -rf github_issue_lifecycle.egg-info')

    # Build and publish
    os.system('python setup.py sdist bdist_wheel')
    os.system('twine upload dist/*')

    sys.exit()

curdir = os.path.dirname(os.path.realpath(__file__))
readme = open(os.path.join(curdir, 'README.md')).read()

setup(
    name='github_issue_lifecycle',
    version='0.1.0',
    description="Serve data on a Github repo's issue history",
    long_description=readme,
    author='Catherine Devlin',
    author_email='catherine.devlin@gsa.gov',
    url='https://github.com/18F/github_issue_lifecycle',
    license="CC0",
    keywords='github issues',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development',
    ],
)
