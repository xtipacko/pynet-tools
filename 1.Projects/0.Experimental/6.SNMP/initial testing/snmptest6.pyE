from pysnmp.hlapi import *
g =  bulkCmd(       SnmpEngine(),
                    UsmUserData('there_was_snmpv3username', 'there_was_snmpv3pa'),
                    UdpTransportTarget(('10.1.1.2', 161)),
                    ContextData(),
                    0, 14,
                    ObjectType(ObjectIdentity('CISCO-AAA-SESSION-MIB', 'casnUserId')),
                    ObjectType(ObjectIdentity('CISCO-AAA-SESSION-MIB', 'casnIpAddr')),
                    lexicographicMode=False)
fulltable = list(g)


print(len(fulltable))

print('\n')
print(('{:<25}'*2).format('casnUserId', 'casnIpAddr')) #fulltable[0][3] or row[3] contains a tupple of ObjectType class' instances or f.e.: *[item[0].prettyPrint()[2:] for item in fulltable[0][3]])
for row in fulltable:
    print (('{:<25}'*2).format(  row[3][0][1].prettyPrint(),
                                 row[3][1][1].prettyPrint()  ) ) # item[0] - name, [1] - value, ?? [2] - index (it is instance of ObjectType class) ; possible to print all at once item.prettyPrint()
                                                      #*[item[1].prettyPrint() for item in row[3]])