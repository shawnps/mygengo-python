# -*- coding: utf-8 -*-
#!/usr/bin/python

from mygengo import MyGengo

# Get an instance of MyGengo to work with...
gengo = MyGengo(
    public_key='your_public_key',
    private_key='your_private_key',
    sandbox=True,  # possibly false, depending on your dev needs
)

# Grab a specific revision - you could liken this to querying version control
# on the Gengo side. :)
print gengo.getTranslationJobRevision(id=42, revision_id=1)
