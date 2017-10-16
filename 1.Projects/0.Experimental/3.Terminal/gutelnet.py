from netmiko import ConnectHandler
import timeit


#start = timeit.default_timer()


def pullvpninfo(brasip,username,password,device_type='cisco_ios_telnet'):
    session = ConnectHandler(device_type='cisco_ios_telnet',
                             ip=brasip,
                             username=username, 
                             password=password)
    #loggedin = timeit.default_timer()
    session.enable()
#enabled = timeit.default_timer()
    session.send_command('terminal size 0')
    vpninfo = session.send_command('show vpdn session all username krugerrr')    
#gottable = timeit.default_timer()
#print(vpdn)
    session.disconnect()
    return vpninfo

if __name__ =='__main__':
    password =''
    with open('pass.ini', 'r') as passfile:
        password = passfile.read()
        passfile.close()
    with open('braslist.ini', 'r') as brasfile:
        braslist = [ bras.rstrip() for bras in brasfile]
        brasfile.close()
    #loaddedini = timeit.default_timer()
    vpninfo = pullvpninfo(braslist[0], 'xtipacko', password)
    print(vpninfo)

#stop = timeit.default_timer()

#information = ('password loading: %.3fs\n' 
#               'logging in      : %.3fs\n'
#               'enabled         : %.3fs\n'
#               'got table       : %.3fs\n'
#               'disconencted    : %.3fs\n')
#print(information %(loaddedini,
#                    loggedin,
#                    enabled,
#                    gottable,
#                    stop))

