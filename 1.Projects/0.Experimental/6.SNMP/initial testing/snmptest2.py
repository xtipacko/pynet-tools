from pysnmp.hlapi import *

queue = [[ObjectType(ObjectIdentity('IF-MIB', 'ifInOctets', 1))],
         [ObjectType(ObjectIdentity('IF-MIB', 'ifOutOctets', 1))]]

iter = getCmd(SnmpEngine(),
              UsmUserData('admin', 'there_was_passwd'),
              UdpTransportTarget(('10.10.10.1', 161)),
              ContextData())

next(iter)

while queue:
    errorIndication, errorStatus, errorIndex, varBinds = iter.send(queue.pop())
    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        for varBind in varBinds:
            print(' = '.join([x.prettyPrint() for x in varBind]))