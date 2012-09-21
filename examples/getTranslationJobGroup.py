# -*- coding: utf-8 -*-
#!/usr/bin/python

from mygengo import MyGengo

# Get an instance of MyGengo to work with...
gengo = MyGengo(
    public_key = 'z~DfqWAxBP#tiuu=A|x0s7PDFdGX#eLldqssiSvl)VK6]gbqJls{9xBxS{W1U|$[',
    private_key = 'wXCC}Wdh1smuGEAWT8VuM6Jb]Sh|Z[D04^nBZGV7G1njU0a0m=-i0xqlp|6V$4h^',

    sandbox = True, # possibly false, depending on your dev needs
    debug = True
)

# Get the job group in question
print gengo.getTranslationJobGroup(id = 16973)
