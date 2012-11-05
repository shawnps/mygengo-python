#!/usr/bin/python

import sys, os
from distutils.core import Command
from setuptools import setup
from setuptools import find_packages
from subprocess import call

__version__ = '1.3.4'

# Command based on Libcloud setup.py:
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
    install_requires = ['requests'],

    # Metadata for PyPI.
    author = 'Gengo',
    author_email = 'api@gengo.com',
    license = 'LGPL License',
    url = 'http://github.com/myGengo/mygengo-python/tree/master',
    keywords = 'gengo translation language api',
    description = 'Official Python library for interfacing with the Gengo API.',
    long_description = open('README.md').read(),
    cmdclass={
        'pep8': Pep8Command,
    },
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet'
    ]
)
