from pysnmp.hlapi import *
import timeit


snmp_engine = SnmpEngine()
usm_auth_data = UsmUserData('there_was_snmpv3username', 'there_was_snmpv3pa')
context = ContextData()

l3devices = [ UdpTransportTarget(('where_was_ip', 161))]

obj = {'casnUserId':ObjectType(ObjectIdentity('CISCO-AAA-SESSION-MIB', 'casnUserId')),
       'casnIpAddr':ObjectType(ObjectIdentity('CISCO-AAA-SESSION-MIB', 'casnIpAddr')),

       'ipCidrRouteDest'   :ObjectType(ObjectIdentity('IP-FORWARD-MIB','ipCidrRouteDest')),
       'ipCidrRouteMask'   :ObjectType(ObjectIdentity('IP-FORWARD-MIB','ipCidrRouteMask')),
       'ipCidrRouteNextHop':ObjectType(ObjectIdentity('IP-FORWARD-MIB','ipCidrRouteNextHop')),
       'ipCidrRouteType'   :ObjectType(ObjectIdentity('IP-FORWARD-MIB','ipCidrRouteType')),
       'ipCidrRouteProto'  :ObjectType(ObjectIdentity('IP-FORWARD-MIB','ipCidrRouteProto')),

       'atIfIndex'         :ObjectType(ObjectIdentity('RFC1213-MIB',    'atIfIndex')),
       'atPhysAddress'     :ObjectType(ObjectIdentity('RFC1213-MIB',    'atPhysAddress')),
       'atNetAddress'      :ObjectType(ObjectIdentity('RFC1213-MIB',    'atNetAddress')) 
       }


stopini = timeit.default_timer()

def printroutingtable(device):
    start = timeit.default_timer()
    bulkquery = bulkCmd(     snmp_engine,
                             usm_auth_data,
                             device,
                             context,
                             0, 15,
                             obj['ipCidrRouteDest'],
                             obj['ipCidrRouteMask'],
                             obj['ipCidrRouteNextHop'],
                             obj['ipCidrRouteType'],
                             obj['ipCidrRouteProto'],
                             lexicographicMode=False)
    routingtable = list(bulkquery)
    stop = timeit.default_timer()
    for row in routingtable:
        index        = row[3][0][0].prettyPrint()
        RouteDest    = row[3][0][1].prettyPrint()
        RouteMask    = row[3][1][1].prettyPrint()
        RouteNextHop = row[3][2][1].prettyPrint()
        RouteType    = row[3][3][1].prettyPrint()
        RouteProto   = row[3][4][1].prettyPrint()
        print('%-25s%-25s%-25s%-25s%-25s' %( RouteDest,
                                             RouteMask,
                                             RouteNextHop,
                                             RouteType,
                                             RouteProto ))
    print('\n')
    print(len(routingtable),'entries')
    print('[%.3fs]'%(stop-start))

def printarptable(device):
    start = timeit.default_timer()
    bulkquery = bulkCmd(     snmp_engine,
                             usm_auth_data,
                             device,
                             context,
                             0, 10,
                             obj['atIfIndex'],
                             obj['atPhysAddress'],
                             obj['atNetAddress'],
                             lexicographicMode=False)
    arptable = list(bulkquery)
    stop = timeit.default_timer()
    for row in arptable:
       # index         = row[3][0][0].prettyPrint()
        atIfIndex     = row[3][0][1].prettyPrint()
        atPhysAddress = row[3][1][1].prettyPrint()
        atNetAddress  = row[3][2][1].prettyPrint()
        print('%-35s%-25s%-25s%-25s' %(      index, atIfIndex,
                                             atPhysAddress,
                                             atNetAddress   ))
    print('\n')
    print(len(routingtable),'entries')
    print('[%.3fs]'%(stop-start))


if __name__ == '__main__':
    #printroutingtable(l3devices[0])
    printarptable(l3devices[0])



#def getroutetable(bras):
#    #start = timeit.default_timer()
#    userfound = False
#    userip = ''
#    brasnumber = None
#    for bras in braslist:        
#        bulkquery = bulkCmd( snmp_engine,
#                             usm_auth_data,
#                             bras,
#                             context,
#                             0, 22,
#                             obj['casnUserId'],
#                             obj['casnIpAddr'],
#                             lexicographicMode=False)
#        for row in bulkquery:
#            if row[3][0][1].prettyPrint() == username:
#                userip = row[3][1][1].prettyPrint()
#                brasnumber = braslist.index(bras)
#                userfound = True
#                return userfound, userip, brasnumber # for found
#    #stop = timeit.default_timer()
#    #print('Search process took: ',round(stop-start, 3), 's' )
#    return userfound, userip, brasnumber # for not found


    
        

    #print('n')
    #print(('{:<25}'*2).format('casnUserId', 'casnIpAddr'))
    #for row in fulltable:
    #    print (('{:<25}'*2).format(  row[3][0][1].prettyPrint(),
    #                                 row[3][1][1].prettyPrint()  ))
    
    #print('Users in total: ', len(fulltable))
#username = '90192'
#userfound, userip, brasnumber = finduser(username,brases)
#if userfound:
#    print('User found on Bras %d\nUser IP is %s' %(brasnumber+1,userip))
#else:
#    print('User %s not found' %username)
