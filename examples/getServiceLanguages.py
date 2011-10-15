# -*- coding: utf-8 -*-
#!/usr/bin/python

from mygengo import MyGengo
from pprint import pprint

mygengo = MyGengo(
    public_key = 'your public key',
    private_key = 'your private key',
    sandbox = False,
	debug = True
)

# Pretty-print a list of every supported language
pprint(mygengo.getServiceLanguages())
