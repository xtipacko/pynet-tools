from pyasn1.type.univ import *
internetId = ObjectIdentifier((1,3,6,1))
print(repr(internetId))
print(internetId[2])
print([x for x in internetId])
internetId[1] = 2