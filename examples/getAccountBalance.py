# -*- coding: utf-8 -*-
#!/usr/bin/python

from mygengo import MyGengo

# Get an instance of MyGengo to work with...
gengo = MyGengo(
    public_key = 'xpU@jqEzqnXCb#OOsAeR4z49IX|j}#dwyliMp2RIq1vM9OIKq-K#{mg~sVBUX^91',
    private_key = '~Q9hI|sV(I^iX7|8WQ=l5=CvUmEWx3[=c5ms09|$JIuT-$aiTIYkS4~1F7^C9dw3',
    sandbox = False, # possibly false, depending on your dev needs
	debug = True
)

# Retrieve and print the account balance. Properties ahoy!
print gengo.getAccountBalance()
