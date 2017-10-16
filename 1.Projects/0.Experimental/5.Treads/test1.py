import threading
import re
from passextr import password
from netmiko import ConnectHandler

class SwitchAccess(threading.Thread):
    def __init__(self, ip, result):
        super(SwitchAccess, self).__init__()
        self.params = { 'device_type' : 'cisco_ios_telnet',
                        'ip'          :  ip,
                        'username'    : 'xtipacko',
                        'password'    :  password,
                        'port'        :  23,
                        'secret'      :  None,
                        'verbose'     :  False               }
        self.result = result
    def run(self):
        try:
            self.connection = ConnectHandler(**self.params)
            self.connection.enable()
            #self.connection.send_command('terminal size 0')
            self.version = self.connection.send_command('show version | i ^.*bytes\ of\ memory.')
            matchobj = re.match('(?P<version>cisco\ \S+)', self.version, flags=re.I)
            if matchobj:
                self.version = matchobj.group('version')
            
            self.hostname = self.connection.find_prompt()[:-1]
            self.result[self.params['ip']] = { 'hostname' : self.hostname, 
                                               'version'  : self.version,
                                               'ip'       : self.params['ip'],
                                               'exception': ''                }
            #self.result.append('{hostname:<32}{ip:<16}{version:<48}{}'.format( hostname = self.hostname,
            #                                                             ip       = self.params['ip'],
            #                                                             version  = self.version       ) )
            self.connection.disconnect()
        except Exception as e:
            self.result[self.params['ip']] = { 'hostname' : 'None', 
                                               'version'  : 'None',
                                               'ip'       : self.params['ip'],
                                               'exception': str(e) }
         

def main():
    result = {}
    print('1')

    switches = [ '93.190.16.%d' %i for i in range(1,254+1) ]
    t = []
    for sw in switches:
        switchthread = SwitchAccess(sw, result)
        switchthread.start()
        t.append(switchthread)
    for switchthread in t:
        switchthread.join()
    
    for switch in sorted(result.keys(), key=lambda ip: int(ip.split('.')[-1])):
        print('{ip:<16}{hostname:<32}{version:<48}{exception}'.format(**result[switch]))

    print('success: %d ' %len(result))


if __name__ == '__main__':
    main()
