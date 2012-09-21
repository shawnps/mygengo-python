#!/usr/bin/python

import sys, os
from setuptools import setup
from setuptools import find_packages

__version__ = '1.3.4'

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
	classifiers = [
		'Development Status :: 4 - Beta',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Topic :: Software Development :: Libraries :: Python Modules',
		'Topic :: Internet'
	]
)
