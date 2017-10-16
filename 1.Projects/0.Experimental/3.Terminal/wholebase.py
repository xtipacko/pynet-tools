from netmiko import ConnectHandler
import timeit
import threading
from pprint import pprint

#start = timeit.default_timer()


def pulltables(brasip,username,password,vpdntables,device_type='cisco_ios_telnet'):
    session = ConnectHandler(device_type='cisco_ios_telnet',
                             ip=brasip,
                             username=username, 
                             password=password)
    #loggedin = timeit.default_timer()
    session.enable()
#enabled = timeit.default_timer()
    session.send_command('terminal size 0')
    vpdn = session.send_command('show vpdn session all')
    vpdntables.append(vpdn)
#gottable = timeit.default_timer()
#print(vpdn)
    session.disconnect()

if __name__ =='__main__':
    password =''
    vpdntables = []
    with open('pass.ini', 'r') as passfile:
        password = passfile.read()
        passfile.close()
    with open('braslist.ini', 'r') as brasfile:
        braslist = [ bras.rstrip() for bras in brasfile]
        brasfile.close()
    #loaddedini = timeit.default_timer()
    threads = []
    for bras in braslist:
        t = threading.Thread(target=pulltables, args=(bras,'xtipacko',password,vpdntables))
        threads.append(t)
        t.start()
    for t in threads:
    	t.join()
    print('symbols', sum([len(table) for table in vpdntables]))
    print('lines', sum([len(table.splitlines()) for table in vpdntables]))
    


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

