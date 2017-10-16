import telnetlib
import re
import errno
from socket import *
from passextr import password
from timeit import default_timer as now
from  dudecsvextractor import extract_devlist
from time import sleep




userprompts = { 'cisco'        : r'Username:\s'.encode('ascii', 'ignore'),
                    'eltex_mes'    : r'User Name:'.encode('ascii', 'ignore'),
                    'eltex_ltp'    : r'Username:\s'.encode('ascii', 'ignore'),
                    'snr'          : r'login:'.encode('ascii', 'ignore'),
                    'snr2970'      : r'Username:\s'.encode('ascii', 'ignore'),
                    'alpha'        : r'Login:'.encode('ascii', 'ignore'),
                    'dlink-dgs'    : r'UserName:'.encode('ascii', 'ignore'),
                    'dlink-dir100' : r'login:\s'.encode('ascii', 'ignore'),      # prof show - shows all config
                    'bdcom'        : r'Username:\s'.encode('ascii', 'ignore'),
                    'mikrotik'     : r'Login:\s'.encode('ascii', 'ignore')
                  }

passprompts = { 'cisco'       : r'Password:\s'.encode('ascii', 'ignore'),
                    'eltex_mes'   : r'Password:'.encode('ascii', 'ignore'),
                    'eltex_ltp'   : r'Password:'.encode('ascii', 'ignore'),
                    'snr'         : r'Password:'.encode('ascii', 'ignore'),
                    'snr2970'     : r'Password:\s'.encode('ascii', 'ignore'),
                    'alpha'       : r'Password:'.encode('ascii', 'ignore'),
                    'dlink-dgs'   : r'PassWord:'.encode('ascii', 'ignore'),
                    'dlink-dir100': r'Password:\s'.encode('ascii', 'ignore'),
                    'bdcom'       : r'Password:\s'.encode('ascii', 'ignore'),
                    'mikrotik'    : r'Password:\s'.encode('ascii', 'ignore')
                  }

authfailmsgs = {'dlink-dgs': r'Fail!'.encode('ascii', 'ignore'),
                'mikrotik'  :r'Login failed'.encode('ascii', 'ignore'),
                'dlink-dir100': r'Login incorrect'.encode('ascii', 'ignore')
               }

authfailregex = b'(?P<fail>'+ b'|'.join([ msg for msg in authfailmsgs.values()]) + b')'

enableprompts = { 'alpha'      : r'Password:'.encode('ascii', 'ignore')
                }
enableregex = b'(?P<enableprompt>'+ b'|'.join([ enableprompt for enableprompt in enableprompts.values()]) + b')'

prompt = r'\n.*(?P<promptsign>#|>)\s?'.encode('ascii') # if here will be problems with banners like ######## or >>>> or else... we can modify prompt

class Genericdev:
    def __init__(self, ip, port, proto='telnet'):
        pass
        #self.connection = None
        #self.prompt = None
        #self.protocol = None
        #self.ip = None
        #self.port = None
        #self.versionmatch = None
        #self.mode = None
    def connect():
        pass
    def disconnect():
        pass
    def auth():
        pass
    def send_command():
        pass # returns result or None 
    def get_version():
        pass
    def change_mode():
        pass
    def current_mode():
        pass


class Generic_classifier:
    
    versions = {'Eltex LTP-4X'                   : { 'vendor':'eltex', 'model':'LTP-4X',  'devicetype': 'l2switch' },
                's72033_rp'                      : { 'vendor':'cisco', 'model':'65xx',    'devicetype': 'l3switch' },
                's222_rp'                        : { 'vendor':'cisco', 'model':'65xx',    'devicetype': 'l3switch' },
                'C3750'                          : { 'vendor':'cisco', 'model':'3750',    'devicetype': 'l3switch' },
                'cat4500'                        : { 'vendor':'cisco', 'model':'45xx',    'devicetype': 'l3switch' },
                'C2950'                          : { 'vendor':'cisco', 'model':'2950',    'devicetype': 'l2switch' },
                'C3550'                          : { 'vendor':'cisco', 'model':'3550',    'devicetype': 'l3switch' },
                'C2940'                          : { 'vendor':'cisco', 'model':'2940',    'devicetype': 'l2switch' },
                'C7301'                          : { 'vendor':'cisco', 'model':'7301',    'devicetype': 'router'   },
                'SNR-S3650G'                     : { 'vendor':'snr',   'model':'3650',    'devicetype': 'l2switch' },
                'SNR-S2940'                      : { 'vendor':'snr',   'model':'2940',    'devicetype': 'l2switch' },
                'SNR-S2970G'                     : { 'vendor':'snr',   'model':'2970',    'devicetype': 'l2switch' }, # show int brief
                'SNR-S2965'                      : { 'vendor':'snr',   'model':'2965',    'devicetype': 'l2switch' },
                'MES2124'                        : { 'vendor':'eltex', 'model':'MES2124', 'devicetype': 'l2switch' },
                'MES1124'                        : { 'vendor':'eltex', 'model':'MES2124', 'devicetype': 'l2switch' },
                'DGS-3120'                       : { 'vendor':'dlink', 'model':'DGS-3120','devicetype': 'l2switch' },
                'DES-3026'                       : { 'vendor':'dlink', 'model':'DES-3026','devicetype': 'l2switch' },
                'DES-3828'                       : { 'vendor':'dlink', 'model':'DES-3026','devicetype': 'l2switch' },
                'DES-3200'                       : { 'vendor':'dlink', 'model':'DES-3200','devicetype': 'l2switch' },
                'DES-3526'                       : { 'vendor':'dlink', 'model':'DES-3526','devicetype': 'l2switch' },
                'Alpha-A28F'                     : { 'vendor':'alpha', 'model':'A28F',    'devicetype': 'l2switch' },
                'P3310B'                         : { 'vendor':'bdcom', 'model':'P3310B',  'devicetype': 'l2switch' },
                'platform: MikroTik'             : { 'vendor':'mikrotik', 'model':'unknown' ,'devicetype': 'l2switch' },
              }

    def __init__(self, ip, authdb, enabledb, timeout=15):
        self.authdb = authdb
        self.enabledb = enabledb
        self.ip = ip
        #scan ports, determine available protocols
        self.ports = None #tmp        

        #logic to choose telnet/ssh/ other proto...        
        self.protocol = None # temporary

        self.connected = False
        self.authenticated = False
        self.climode = 'unknown' # 'user' >, 'privileged' #, 'config' (config)
        self.timeout = timeout        
 
        #candidates to be methods:
        self.prompt = None
        self.versionmatch = 'unknown'
        self.showversion = None
        self.vendor = 'unknown'
        self.model = 'unknown'
        self.devicetype = 'unknown' # router, l2switch, l3switch, nix, 

    def parse_version(self, commandoutput):                
        if self.vendor == 'mikrotik':
            match = re.match(r'[\s\S]*board-name:\ (?P<model>[a-zA-Z0-9-_.\ ]*)(\n|\r\n)'.encode(), commandoutput)
            if match:
                self.model = match.group('model').decode('utf-8', 'ignore')
                self.showversion = commandoutput
        else:
            for version in self.versions.keys():                
                if version.encode('ascii', 'ignore') in commandoutput:
                    self.showversion = commandoutput
                    self.versionmatch = version                
                    break         
    
    def __str__(self):
        return f'{self.vendor} {self.model}'
        
        # THIS BLOCK GOES TO  dispatcher
        #if 'telnet' in self.protocol:
        #    self.telnet_classification(self.ports[0]) #we can try each port
        #
        #if 'ssh' in self.protocol and self.versionmatch == 'unknown':
        #    self.ssh_classification(self.ports[1]) #we can try each port)         

class Telnet_classifier(Generic_classifier):

    def __init__(self, ip, authdb, enabledb=[''], port=23, timeout=15):
        super().__init__(ip, authdb, enabledb, timeout)
        #tmp check -- will be transsfered to higher level loginc
        try:
            self.checkport(port)
        except:
            return

        try:
            self.classify(port)
        except:
            pass
        finally:
            if self.connected:
                self.disconnect()

        if self.vendor == 'unknown' and self.model == 'unknown':
            try:
                self.classifydir100()
            except:
                pass
            finally:
                if self.connected:
                    self.disconnect()


    def checkport(self, port):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.settimeout(2)
        error = sock.connect_ex((self.ip, port))
  
        if (error == errno.WSAEWOULDBLOCK or
            error == errno.WSAECONNREFUSED or
            error == errno.EWOULDBLOCK or
            error == errno.WSAECONNREFUSED):
            print(errno.errorcode[error], error)
            raise Exception(f'port {port} is closed')
            


    def testcallback(self, sock, cmd, opt): # for dir 100
        if cmd == telnetlib.DO and opt == telnetlib.TTYPE:
            sock.sendall(b'\xff\xfb\x1f\xff\xfb\x20\xff\xfb\x18\xff\xfb\x27\xff\xfd\x01\xff\xfb\x03\xff\xfd\x03')
            sleep(.01)
            sock.sendall(b'\xff\xfa\x18\x00\x58\x54\x45\x52\x4d\xff\xf0')
            sleep(.01)
            sock.sendall(b'\xff\xfb\x24')


    def connect(self, port):
        try:
            if not self.connected:
                self.telcon = telnetlib.Telnet(self.ip, port)
                self.connected = True
        except Exception as e:
            if not self.connected:
                self.connected = False
                raise e
            else:
                raise Exception('Already connected')

    def classifydir100(self): # an exceptional device
        self.connect(23)
        self.telcon.option_callback = self.testcallback
        self.classify(23)

    def classify(self, port):
        if not self.connected:
            self.connect(port)

        for authdata in self.authdb:  # Trying to select correct username + password
            self.auth(*authdata)
            if self.authenticated: break
        else: 
            raise Exception('Authentication failed')

        
        if self.climode == 'user': 
            for enablepass in self.enabledb:
                self.enable(enablepass)
                if self.climode == 'priviledged': break # Trying to select correct password for priviledged mode
            else:
                raise Exception('Priviledged mode authentication failed')
                

        self.disable_scrolling()

        self.get_version()
        if self.versionmatch != 'unknown':
            self.vendor = self.versions[self.versionmatch]['vendor']
            self.model = self.versions[self.versionmatch]['model']
            self.devicetype = self.versions[self.versionmatch]['devicetype']
        self.disconnect()
        return self.versionmatch

    def enable(self, password):
        self.enablepass = password
        try:
            self.change_mode('priviledged')
        except:
            return False
        return True

    def change_mode(self, mode):
        if mode == 'priviledged':
            self.telcon.write(b'enable\r\n')
            match = self.telcon.expect([enableregex, prompt], 2)
            self.telcon.write(b'\r\n')
            self.telcon.expect([prompt], 2) # add ramification to handle such cases for other devices (Cisco, etc...)            
            # check if successfull, if not raise Exception
            self.climode = 'priviledged'

    def preauth_classification(self, matchedstr):
        if b'MikroTik' in matchedstr:
            self.vendor = 'mikrotik'
            self.climode = 'priviledged'    
        elif b'DIR-100' in matchedstr:
            self.vendor = 'dlink'
            self.model = 'DIR-100'
            self.climode = 'priviledged'
            self.telcon.write(b'admin\r\n') # protect them from lags
            sleep(.01)
            self.telcon.write(b'310908\r\n')
            sleep(.01)
            self.telcon.write(b'logout\r\n')
            sleep(.01)
            self.telcon.close()
            self.connected = False
            raise Exception('for D-LINK DIR-100 authentication is not Implemented') 
        elif b'D-Link' in matchedstr:
            self.vendor = 'dlink'
            self.climode = 'priviledged'
        elif b'SWH-3614F' in matchedstr:
            self.vendor = 'swh'
            self.model = 'SWH-3614F'
            raise Exception('for SWH-3614F authentication is not Implemented') 
        elif b'TDMoIP' in matchedstr:
            self.vendor = 'natex (or rad)'
            raise Exception('for SDH/PDH TDMoIP devices authentication is not Implemented') 
        elif b'IPmux' in matchedstr:
            self.vendor = 'rad'
            raise Exception('for SDH/PDH IPmux devices authentication is not Implemented') 
        

    def auth(self, username, password):
        _,_,matchedstr = self.telcon.expect(list(userprompts.values()), 2)
        self.preauth_classification(matchedstr)  

        if self.vendor == 'mikrotik': #to catch first classification 
            username = f'{username}+ct'
        
        self.telcon.write(b'%s\r\n' %username.encode('ascii', 'ignore'))
        match2 = self.telcon.expect(list(passprompts.values()), 2)        
        self.telcon.write(b'%s\r\n' %password.encode('ascii', 'ignore'))
        _, match, _ = self.telcon.expect([prompt, authfailregex], self.timeout)   
        if not match:
            self.authenticated = False
            return
        matchd = match.groupdict()
        if 'promptsign' in matchd:
            if matchd['promptsign'] == b'>':
                self.authenticated = True
                if self.climode != 'priviledged': # a bit incorrect handling in preauth_classification
                    self.climode = 'user'
            elif matchd['promptsign'] == b'#':
                self.authenticated = True
                self.climode = 'priviledged'
        elif 'fail' in matchd:
            if matchd['fail'] in authfailmsgs.values():
                self.authenticated = False
        else:
            self.authenticated = False
            raise Exception('auth, unexpected behavior, neither known promptsigns nor fail messages found')
        
    def disable_scrolling(self):
        if self.vendor in ['cisco', 'snr', 'unknown',
                           'bdcom', ]:
            self.telcon.write(b'terminal length 0\r\n')
            self.telcon.expect([prompt], self.timeout)
        if self.vendor == 'alpha':
            self.telcon.write(b'terminal page-break disable\r\n')
            self.telcon.expect([prompt], self.timeout)

    def get_version(self): 
        if self.vendor == 'unknown':
            get_ver_commands = [ b'show version\r\n',
                                 b'show unit\r\n', 
                                 b'system resource print\r\n',
                                 b'show switch\r\n',                                                             
                                 b'?\r\n'                    ]
        elif self.vendor == 'mikrotik':
            get_ver_commands = [ b'system resource print\r\n']
        elif self.vendor == 'dlink':
            get_ver_commands = [ b'show switch\r\n',                                                             
                                 b'?\r\n'                    ]
        else:
            raise Exception('Undefined Vendor')

        
        for command in get_ver_commands: # try every command to determine version
            self.telcon.write(command)
            output = self.telcon.expect([prompt, r'Next\ Entry'.encode()], 1) #Next Entry for dlink DES/DGS            
            self.parse_version(output[2]) #.decode removed
            if self.versionmatch != 'unknown': 
                break

    def disconnect(self):
        self.telcon.close()
        self.connected = False


def main():
    authdb = [ ('xtipacko', password),
               ('admin', '310908' )
             ] # + Nortels
    # start = now()
    

    # print(Telnet_classifier('where_was_ip', authdb))


 

  

    # stop = now() - start
    # print(f'[{stop:.3f} sec.]')

    netwdevs = extract_devlist()
    print('{:<20}{:<48}{:<32}{:<32}'.format('-IP ADDRESS-', '-DUDE\'s NAME-', '-IP ADDRESS LIST-', '-VERSION-'))

    show = ( '{dev:<20}{name:<48}{iplist!s:<32}{version!s:<32}'.format( dev     = dev,
                                                                         name    = netwdevs[dev]["dude_name"],
                                                                         iplist  = netwdevs[dev]["dude_iplist"],
                                                                         version = Telnet_classifier(dev, authdb) ) 
              for dev in netwdevs.keys()                                                                             )
    for dev in show:
        print(dev)


if __name__ == '__main__':
    main()
