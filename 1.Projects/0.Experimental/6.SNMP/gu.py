#gu stands for Get User's session from BRAS
import timeit
mainstart = timeit.default_timer()
from pysnmp.hlapi import *
from customsnmpdata import *
from macvendors import mac_lookup
from passextr import password
from ipaddress import *
from netmiko import ConnectHandler
#from queue import Queue
from colorama import Fore
from colorama import init as initcolor
import pymysql
import threading
import codecs
import sys
import re
import os

# -*- coding: utf-8 -*-

def check_on_bras(username, bras):
    brasnumber = braslist.index(bras) 
    bulkquery = bulkCmd( SnmpEngine(),
                         usm_user_data,
                         bras,
                         context,
                         0, 22,
                         obj['casnUserId'],
                         lexicographicMode=False)
    for row in bulkquery:
        if result: # for one result optimisation
            break
        gotusername = row[3][0][1].prettyPrint()
        tableindex = row[3][0][0].prettyPrint()
        if  gotusername == username:
            result.append((tableindex, brasnumber) )#ADD LOCK!
            break

def query_db_for_user(username):
    table_name = 'sessions'
    try:
        connection = pymysql.connect(host='localhost', 
                                     user='root',
                                     password=password,
                                     charset='utf8mb4',
                                     database='pptpclients',
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            qSELECT_USER = ('SELECT username,aaausersnmpindex,brasip FROM {table_name}\n'
                            'WHERE username="{username}";'.format(table_name=table_name, username=username))
            cursor.execute(qSELECT_USER)
            userdata = cursor.fetchall()
            return userdata
    except:
        raise Exception('unknown problem during db access')
    finally:
        connection.close()

def check_if_user_actual(usersqlinfo):
    if not usersqlinfo:
        return False
    try:
        userindex = int(usersqlinfo[0]['aaausersnmpindex'])
    except ValueError:
        return False
    except KeyError:
        print('debug message: unknown error in check_if_user_actual, key aaausersnmpindex doesn`t exist')
    except:
        print('debug message: unknown error in check_if_user_actual')
    if not userindex:
        return False
    brasnumber = brasiptonum[usersqlinfo[0]['brasip']]
    bras = braslist[brasnumber]    
    username = usersqlinfo[0]['username']
    try:
        snmpquery = getCmd( SnmpEngine(),
                            usm_user_data,
                            bras,
                            context,
                            ObjectType(ObjectIdentity('CISCO-AAA-SESSION-MIB', 'casnUserId', userindex)) )
        errorIndication, errorStatus, errorIndex, values = next(snmpquery)
        if (values[0][1].prettyPrint() == username):
            return True
        else:
            return False
    except:
        #print('debug message: unknown issue in check_if_user_actual procedure')
        return False
def finduser(username):
    user = query_db_for_user(username)
    if check_if_user_actual(user):
        result.append( (user[0]['aaausersnmpindex'], brasiptonum[user[0]['brasip']]) )
    else:
        threads = []
        for bras in braslist:
            t = threading.Thread(target=check_on_bras, args=(username, bras))
            t.daemon = True
            t.start()
            threads.append(t)
        for t in threads:
            t.join()

def vpn_subnet_identifier(tunnelremoteip, vpn_subnets):
    try:
        for subnet in vpn_subnets['vpn']:
            if IPv4Address(tunnelremoteip) in IPv4Network(subnet):
                return  Fore.GREEN + 'OK' + Fore.RESET
        for subnet in vpn_subnets['blocked']:
            if IPv4Address(tunnelremoteip) in IPv4Network(subnet):
                return Fore.MAGENTA + 'BLOCKED' + Fore.RESET
    except AddressValueError:
        return '[vpn_subnet_identifier():%s invalid ip address]' %tunnelremoteip
    return 'Unknown Subnet'

def printKVs(key, values, timing=True, separator=' ', adjusttime=0):
    if type(values) is list:
        values = separator.join(values)
    time = ''
    adjusttime *= ' '
    if timing:
        time = timeit.default_timer() - mainstart
        time = '{adjust}[{}{:.3f}{}s]'.format(Fore.YELLOW, time, Fore.RESET, adjust=adjusttime)
    line = '  {key:<17}: {values:<35} {time}'.format( key        = key, 
                                                      values     = values, 
                                                      time       = time    )
    print(line)

def printinfo(result, username, password):
    bras_excerpt = result[0]
    tableindex, brasnumber = bras_excerpt
    tableindex = int(tableindex.split('.')[-1])#last value after . delimeter in oid
    friendlybrasnumber = brasnumber+1 #for printing
    print(' {username} on Bras {brasnumber}'.format(username   = Fore.YELLOW + username + Fore.RESET,
                                                    brasnumber = friendlybrasnumber))
    tunnelremoteip = request_tunnel_remote_ip(tableindex, braslist[brasnumber])
    subnet_purpose = vpn_subnet_identifier(tunnelremoteip, vpn_subnets)
    printKVs('Tunnel Remote IP', [tunnelremoteip, '(VPN %s)' %subnet_purpose], adjusttime=10)
    session = prep_bras_ses(brasiplist[brasnumber])
    vpdn_tun_info = get_tun_info(username, session)
    vpdn_tun_info_dict = parse_show_vpdn_ses(vpdn_tun_info)
    printKVs('Session time', vpdn_tun_info_dict['sessiontime'])
    printKVs('Interface name', vpdn_tun_info_dict['interfacename'])
    nexthop_to_source = get_nexthop(vpdn_tun_info_dict['tunelsourceip'], session)
    l3ipaddr = nexthop_to_source # REPLACE WITH MORE COMPLEX FUNCTION
    printKVs('Tunnel Source IP', [vpdn_tun_info_dict['tunelsourceip'], '(via %s)' %l3ipaddr])
    client_mac_address = get_client_mac(vpdn_tun_info_dict['tunelsourceip'], 
                                        l3ipaddr, 
                                        adminusername, 
                                        password)
    printKVs('MAC Address', client_mac_address)
    client_vendor = mac_lookup(client_mac_address)
    printKVs('Vendor', client_vendor)
    session.disconnect()

def request_tunnel_remote_ip(userindex, bras):
    snmpquery = getCmd( SnmpEngine(),
                        usm_user_data,
                        bras,
                        context,
                        ObjectType(ObjectIdentity('CISCO-AAA-SESSION-MIB', 'casnIpAddr', userindex)) )
    errorIndication, errorStatus, errorIndex, values = next(snmpquery)
    return values[0][1].prettyPrint()

def prep_bras_ses(brasip):
    session = ConnectHandler(device_type='cisco_ios_telnet',
                             ip=brasip,
                             username=adminusername,
                             password=password)
    return session

def get_tun_info(username, session):
    session.enable()
    session.send_command('terminal size 0')
    show_vpdn_user = 'show vpdn session all username %s' %username
    show_output = session.send_command(show_vpdn_user)
    return show_output

def parse_show_vpdn_ses(command_output):
    matchobj = re.match(r'[\s\S]*Internet\ Address\ is\ (.*)[\s\S]*'
                        r'Time\ since\ change\ (.*),'
                        r'\ interface\ Vi(.*)[\s\S]*', command_output)
    vpdn_tun_info_dict = {'tunelsourceip': matchobj.group(1),
                          'sessiontime'  : matchobj.group(2),
                          'interfacename': 'Virtual-Access' + matchobj.group(3) }
    return vpdn_tun_info_dict

def get_nexthop(targetip,session):
    '''primitive procedure, when it parses route, it will not consider ecmp routes'''
    show_ip_route_output = session.send_command('show ip route '+ targetip)
    matchobj = re.match(r'[\s\S]*'
                        r'Routing Descriptor Blocks:\n'
                        r'[\s*]*(.*), from', show_ip_route_output)
    return matchobj.group(1)

def get_client_mac(tunnelsource, l3ipaddr, adminusername, password):
    session = ConnectHandler(device_type='cisco_ios_telnet',
                             ip=l3ipaddr,
                             username=adminusername,
                             password=password)
    session.enable()
    arp = session.send_command('show ip arp %s' %tunnelsource)
    session.disconnect()
    return parse_show_ip_arp(arp)

def parse_show_ip_arp(command_output):
    matchobj = re.match(r'Protocol.+\n'
                        r'(.+?)\ +(.+?)\ +(.+?)\ +(.+?)\ +(.+?)',command_output)
    return matchobj.group(4)#tmp

if __name__ == '__main__':
    #entry point here
    initcolor()
    print('Get User v0.13')
    if len(sys.argv) < 2:
        print('\n') 
        print('You forgot to specify username')
        exit()
    elif len(sys.argv) > 2:
        print('\n') 
        print('Theese are extra arguments:', ', '.join(sys.argv[2:]))
    username = sys.argv[1]
    adminusername = 'xtipacko'
    result = [] # [(tunnelremoteip, brasnumber),...]
    usm_user_data = UsmUserData('there_was_snmpv3username', 'there_was_snmpv3password')
    context = ContextData()
    print('Checking vpn session for %s on BRASes: 1 - %d' %(username, len(braslist)))
    finduser(username)    
    if result:
        print('\n') 
        printinfo(result, username, password)
    else:    
        print('\n')
        print('%s User %s%s %snot found%s' %(Fore.LIGHTMAGENTA_EX, Fore.RESET, username, Fore.LIGHTMAGENTA_EX, Fore.RESET))
    
#mainstop = timeit.default_timer()
#print('\n\n[%.3fs]' %(mainstop - mainstart))
