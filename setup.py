#!/usr/bin/python

import sys, os
from distutils.core import Command
from setuptools import setup
from setuptools import find_packages
from subprocess import call

__author__ = 'Ryan McGrath <ryan@mygengo.com>'
__version__ = '1.3.3'

# Commands based on Libcloud setup.py:
# https://github.com/apache/libcloud/blob/trunk/setup.py

class Pep8Command(Command):
    description = "Run pep8 script"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            import pep8
            pep8
        except ImportError:
            print ('Missing "pep8" library. You can install it using pip: '
                   'pip install pep8')
            sys.exit(1)

        cwd = os.getcwd()
        retcode = call(('pep8 %s/mygengo/' % (cwd)).split(' '))
        sys.exit(retcode)

setup(
    # Basic package information.
    name = 'mygengo',
    version = __version__,
    packages = find_packages(),

    # Packaging options.
    include_package_data = True,

    # Package dependencies.
    install_requires = ['simplejson'],

    # Metadata for PyPI.
    author = 'Ryan McGrath',
    author_email = 'ryan@venodesigns.net',
    license = 'LGPL License',
    url = 'http://github.com/ryanmcgrath/mygengo/tree/master',
    keywords = 'mygengo translation language api japanese english',
    description = 'Official Python library for interfacing with the MyGengo API.',
    long_description = open('README.md').read(),
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Communications :: Chat',
        'Topic :: Internet'
    ],
    cmdclass={
        'pep8': Pep8Command
    }
)
