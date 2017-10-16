from pysnmp.hlapi import *
from time import sleep
g =  bulkCmd(             SnmpEngine(),
                          UsmUserData('there_was_snmpv3username', 'there_was_snmpv3pa'),
                          UdpTransportTarget(('where_was_ip', 161)),
                          ContextData(),
                          0, 14,
                          ObjectType(ObjectIdentity('IF-MIB', 'ifIndex')),
                          ObjectType(ObjectIdentity('IF-MIB', 'ifDescr')),
                          ObjectType(ObjectIdentity('IF-MIB', 'ifSpeed')),
                          ObjectType(ObjectIdentity('IF-MIB', 'ifAdminStatus')),
                          ObjectType(ObjectIdentity('IF-MIB', 'ifOperStatus')),
                          lexicographicMode=False)
fulltable = list(g)


print(len(fulltable))
print('\n')
print(('{:<25}'*5).format(*[item[0].prettyPrint()[8:-2] for item in fulltable[0][3]])) #fulltable[0][3] or row[3] contains a tupple of ObjectType class' instances
for i, row in enumerate(fulltable):
    print (('{:<25}'*5).format(row[3][0][1].prettyPrint(),
                                                   row[3][1][1].prettyPrint(),
                                                   int(row[3][2][1]) // 1000000,
                                                   row[3][3][1].prettyPrint(),
                                                   row[3][4][1].prettyPrint()
                                                  ) ) # item[0] - name, [1] - value, ?? [2] - index (it is instance of ObjectType class) ; possible to print all at once item.prettyPrint()
                                                      #*[item[1].prettyPrint() for item in row[3]])