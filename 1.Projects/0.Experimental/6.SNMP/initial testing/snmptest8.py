from pysnmp.hlapi import *
import timeit
from time import sleep
startini = timeit.default_timer()
snmp_engine = SnmpEngine()
usm_auth_data = UsmUserData('there_was_snmpv3username', 'there_was_snmpv3pa')
context = ContextData()

obj = {'casnUserId':ObjectType(ObjectIdentity('CISCO-AAA-SESSION-MIB', 'casnUserId')),
       'casnIpAddr':ObjectType(ObjectIdentity('CISCO-AAA-SESSION-MIB', 'casnIpAddr')),

       'cvpdnSessionAttrUserName':ObjectType(ObjectIdentity('CISCO-VPDN-MGMT-MIB', 'cvpdnSessionAttrUserName')),

       'cvpdnTunnelAttrRemoteIpAddress': ObjectType(ObjectIdentity('CISCO-VPDN-MGMT-MIB', 'cvpdnTunnelAttrRemoteIpAddress')),
       'cvpdnSessionAttrUserName': ObjectType(ObjectIdentity('CISCO-VPDN-MGMT-MIB', 'cvpdnSessionAttrUserName')),
       'cvpdnTunnelAttrTunnelId': ObjectType(ObjectIdentity('CISCO-VPDN-MGMT-MIB', 'cvpdnTunnelAttrTunnelId')),       
       'cvpdnTunnelAttrRemoteTunnelId': ObjectType(ObjectIdentity('CISCO-VPDN-MGMT-MIB', 'cvpdnTunnelAttrRemoteTunnelId')),
       'cvpdnTunnelAttrLocalName': ObjectType(ObjectIdentity('CISCO-VPDN-MGMT-MIB', 'cvpdnTunnelAttrLocalName')),
       'cvpdnTunnelAttrRemoteName': ObjectType(ObjectIdentity('CISCO-VPDN-MGMT-MIB', 'cvpdnTunnelAttrRemoteName')),
       'cvpdnTunnelAttrRemoteEndpointName': ObjectType(ObjectIdentity('CISCO-VPDN-MGMT-MIB', 'cvpdnTunnelAttrRemoteEndpointName')),
       'cvpdnTunnelAttrLocalInitConnection': ObjectType(ObjectIdentity('CISCO-VPDN-MGMT-MIB', 'cvpdnTunnelAttrLocalInitConnection')),
       'cvpdnTunnelAttrOrigCause': ObjectType(ObjectIdentity('CISCO-VPDN-MGMT-MIB', 'cvpdnTunnelAttrOrigCause')),
       'cvpdnTunnelAttrState': ObjectType(ObjectIdentity('CISCO-VPDN-MGMT-MIB', 'cvpdnTunnelAttrState')),
       'cvpdnTunnelAttrActiveSessions': ObjectType(ObjectIdentity('CISCO-VPDN-MGMT-MIB', 'cvpdnTunnelAttrActiveSessions')),
       'cvpdnTunnelAttrDeniedUsers': ObjectType(ObjectIdentity('CISCO-VPDN-MGMT-MIB', 'cvpdnTunnelAttrDeniedUsers')),
       'cvpdnTunnelAttrSoftshut': ObjectType(ObjectIdentity('CISCO-VPDN-MGMT-MIB', 'cvpdnTunnelAttrSoftshut')),
       'cvpdnTunnelAttrNetworkServiceType': ObjectType(ObjectIdentity('CISCO-VPDN-MGMT-MIB', 'cvpdnTunnelAttrNetworkServiceType')),
       'cvpdnTunnelAttrLocalIpAddress': ObjectType(ObjectIdentity('CISCO-VPDN-MGMT-MIB', 'cvpdnTunnelAttrLocalIpAddress')),
       'cvpdnTunnelAttrSourceIpAddress': ObjectType(ObjectIdentity('CISCO-VPDN-MGMT-MIB', 'cvpdnTunnelAttrSourceIpAddress')),
       'cvpdnTunnelAttrRemoteIpAddress': ObjectType(ObjectIdentity('CISCO-VPDN-MGMT-MIB', 'cvpdnTunnelAttrRemoteIpAddress')),
       'cvpdnTunnelAttrLocalInetAddressType': ObjectType(ObjectIdentity('CISCO-VPDN-MGMT-MIB', 'cvpdnTunnelAttrLocalInetAddressType')),
       'cvpdnTunnelAttrLocalInetAddress': ObjectType(ObjectIdentity('CISCO-VPDN-MGMT-MIB', 'cvpdnTunnelAttrLocalInetAddress')),
       'cvpdnTunnelAttrSourceInetAddressType': ObjectType(ObjectIdentity('CISCO-VPDN-MGMT-MIB', 'cvpdnTunnelAttrSourceInetAddressType')),
       'cvpdnTunnelAttrSourceInetAddress': ObjectType(ObjectIdentity('CISCO-VPDN-MGMT-MIB', 'cvpdnTunnelAttrSourceInetAddress')),
       'cvpdnTunnelAttrRemoteInetAddressType': ObjectType(ObjectIdentity('CISCO-VPDN-MGMT-MIB', 'cvpdnTunnelAttrRemoteInetAddressType')),
       'cvpdnTunnelAttrRemoteInetAddress': ObjectType(ObjectIdentity('CISCO-VPDN-MGMT-MIB', 'cvpdnTunnelAttrRemoteInetAddress'))
       }

lbras = [ None,
         UdpTransportTarget(('where_was_ip', 161)),
         UdpTransportTarget(('10.1.1.2', 161)),
         UdpTransportTarget(('10.1.1.3', 161)),
         UdpTransportTarget(('10.1.1.4', 161)),
         UdpTransportTarget(('10.1.1.5', 161)),
         UdpTransportTarget(('10.1.1.6', 161))]
stopini = timeit.default_timer()

def printallusers(bras):
    start = timeit.default_timer()
    gen = bulkCmd( snmp_engine,
                   usm_auth_data,
                   bras,
                   context,
                   0, 22,
                   obj['casnUserId'],
                   obj['casnIpAddr'],
                   #obj['cvpdnSessionAttrUserName'],
                   #obj['cvpdnTunnelAttrTunnelId'],
                   #obj['cvpdnTunnelAttrRemoteTunnelId'],
                   #obj['cvpdnTunnelAttrLocalName'],
                   #obj['cvpdnTunnelAttrRemoteName'],
                   #obj['cvpdnTunnelAttrRemoteEndpointName'],
                   #obj['cvpdnTunnelAttrLocalInitConnection'],
                   #obj['cvpdnTunnelAttrOrigCause'],
                   #obj['cvpdnTunnelAttrState'],
                   #obj['cvpdnTunnelAttrActiveSessions'],
                   #obj['cvpdnTunnelAttrDeniedUsers'],
                   #obj['cvpdnTunnelAttrSoftshut'],
                   #obj['cvpdnTunnelAttrNetworkServiceType'],
                   #obj['cvpdnTunnelAttrLocalIpAddress'],
                   #obj['cvpdnTunnelAttrSourceIpAddress'],
                   #obj['cvpdnTunnelAttrRemoteIpAddress'],
                   #obj['cvpdnTunnelAttrLocalInetAddressType'],
                   #obj['cvpdnTunnelAttrLocalInetAddress'],
                   #obj['cvpdnTunnelAttrSourceInetAddressType'],
                   #obj['cvpdnTunnelAttrSourceInetAddress'],
                   #obj['cvpdnTunnelAttrRemoteInetAddressType'],
                   #obj['cvpdnTunnelAttrRemoteInetAddress'],
                   lexicographicMode=False)
    fulltable = list(gen)
    stop = timeit.default_timer()
    print('n')
    print(('{:<35}'*2).format('forIndex','cvpdnTunnelAttrRemoteIpAddress'))
    for i, row in enumerate(fulltable):
        print (('{:<35}'*2).format(  i,
                                     row[3][0][1].prettyPrint() ))
        #print(row)
    print('Snmp query took:  ', round(stop-start, 3), 's' )
    print('Users in total: ', len(fulltable))


printallusers(lbras[1])
#for i in range(60):
#    print('Users in total: ', printallusers(lbras[4]))
#    sleep(60)

#print('Initialisation took:', round(stopini - startini), 's')