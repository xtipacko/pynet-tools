from netconnect.connection.classification import device_types, con_protocols, device_roles
from netconnect.errors import *
from telnetlib import Telnet
import re
import logging
import netconnect.logaux as logaux

#from timeit import default_timer as now

PROMPT = r'\n(?P<prompt>\S*)(?P<promptsign>#|>)\ ?'.encode('ascii')
PROMPTc = re.compile(PROMPT, flags=re.M)

LOGINPROMPT = r'(?P<loginprompt>(user\ ?name|login):\ ?)'.encode('ascii')
LOGINPROMPTc = re.compile(LOGINPROMPT, flags=re.I)

PASSPROMPT = r'(?P<passprompt>password:\ ?)'.encode('ascii') 
PASSPROMPTc = re.compile(PASSPROMPT, flags=re.I)

ENABLEPROMPT = r'(?P<enableprompt>password:\ ?)'.encode('ascii')
ENABLEPROMPTc = re.compile(ENABLEPROMPT, flags=re.I)

AUTHFAIL = r'(?P<failmessage>[\s\S]*(\ fail|\ incorrect|\ invalid)[\s\S]*)'.encode('ascii')
AUTHFAILc = re.compile(AUTHFAIL, flags=re.I|re.M)

tENTER = b'\r\n' # Enter for telnet


class Connection(object):    
    def __init__(self, host, username, password, **kwargs):      
        whoami = type(self).__name__
        logging.debug(f'  INSTANCE OF {whoami} CREATED: host = {host}, username = {username}')
        self.host = host
        self.port = kwargs.get('port', 23)
        self.username = username.encode('ascii')
        self.password = password.encode('ascii')
        self.socket = None
        self.connected = False # to-do: make it a property, reflecting state of socket if possible
        self.authenticated = False
        self.global_timeout = kwargs.get('global_timeout', 2)
        self.prompt = None
        self.promptsign = None
        self.banner = None

        self.rPROMPT       = PROMPTc
        self.rLOGINPROMPT  = LOGINPROMPTc
        self.rPASSPROMPT   = PASSPROMPTc
        self.rENABLEPROMPT = ENABLEPROMPTc
        self.rAUTHFAIL     = AUTHFAILc
        
        protocol = kwargs.get('protocol', 'tel')
        if protocol in con_protocols:
            self.protocol = protocol
        else:
            raise Exception(f'No such connection protocol: {protocol}')

        device_type = kwargs.get('device_type', 'generic')
        if device_type in device_types:
            self.device_type = device_type
        else:
            raise Exception(f'No such device type: {device_type}')

        device_role = kwargs.get('device_role', 'l2')
        if device_role in device_roles:
            self.device_role = device_role
        else:
            raise Exception(f'No such device role: {device_role}')

        auto_connect = kwargs.get('auto_connect', True )
        if auto_connect:
            logging.debug(f'AUTO CONNECTION: ({self.host}:{self.port})')
            self.connect()


    def connect(self):
        logging.debug(f'{logaux.generic} {logaux.con}: to {self.host}:{self.port}.')
        if self.protocol == 'tel':
            self.connect_tel()
        else:
            self.connect_ssh()

        if not self.authenticated:
            logging.debug(f'           AUTH WILL BE STARTED: ({self.host}:{self.port}) username = {self.username}')
            self.auth()


    def connect_ssh():
        raise NotImplemented()
        try:
            # to-do: try to connect
            self.authenticated = True
        except: # to-do: determine exception types
            pass


    def connect_tel(self):
        logging.debug(f'{logaux.telnet} {logaux.con}: to {self.host}:{self.port}.')
        try:
            self.connection = Telnet(host=self.host, port=self.port, timeout=self.global_timeout)
            self.socket = self.connection.get_socket()
            self.connected = True
            logging.debug(f'{logaux.telnet} {logaux.con}: ({self.host}:{self.port}) SUCCESSFUL.')
        except: # to-do: determine exception types
            self.connected = False
            logging.debug(f'{logaux.telnet} {logaux.con}: ({self.host}:{self.port}) UNSUCCESSFUL.')


    def send_command(self, command, **kwargs):        
        logging.debug(f'{logaux.generic} {logaux.sending}: ({self.host}:{self.port}) command: "{command}"')
        expect  = kwargs.get('expect',  self.rPROMPT)
        timeout = kwargs.get('timeout', self.global_timeout)
        if not self.connected:
            self.connect()  #trying to connect
            if not self.connected:
                logging.debug(f'{logaux.generic} {logaux.sending}: ({self.host}:{self.port}) command: "{command}" UNSUCCESSFUL, can not connect')
                raise Exception('can not connect')
        if not self.authenticated:
            logging.debug(f'{logaux.generic} {logaux.sending}: ({self.host}:{self.port}) command: "{command}" UNSUCCESSFUL, not authenticated')
            raise Exception('not authenticated')
            

        if self.protocol == 'tel':
            return self.send_command_tel(command, expect, timeout)
        elif self.protocol == 'ssh':
            raise Exception('Base_class - send_command for ssh not implemented yet')
    

    def send_command_tel(self, command, expect, timeout):
        logging.debug(f'{logaux.telnet} {logaux.sending}: ({self.host}:{self.port}) "{command}" , expecting: {expect.pattern}, with timeout {timeout}s.')
        try:
            self.connection.write(command.encode('ascii', 'ignore') + tENTER)
            logging.debug(f'{logaux.telnet} {logaux.snt}: ({self.host}:{self.port})  "{command}" ')
            _, m, output = self.connection.expect([expect], timeout)
            outputln = len(output)
            logging.debug(f'{logaux.telnet} {logaux.rcvd}: ({self.host}:{self.port}) for "{command}" received answer, length {outputln} bytes.')
        except (ConnectionAbortedError, EOFError):
            self.connected = False
            self.authenticated = False
            self.connect()
            if self.connected and self.authenticated: # try one more time
                self.connection.write(command.encode('ascii', 'ignore') + tENTER)
                _, _, output = self.connection.expect([expect], timeout)   
            elif not self.connected:
                raise Exception('can not reconnect')
            elif self.connected and not self.authenticated:
                raise Exception('reconnected, but can not reauthenticate')
        #timestamp = now() - start
        #print(f'command {command} take {timestamp:.3f}s')
        output = output.replace(b'\r\n', b'\n').decode('utf-8', 'ignore')
        logging.debug(f'{logaux.telnet} {logaux.snt}: ({self.host}:{self.port}) for "{command}" decoded answer is:\n{output}')
        if output and '\n' in output:
            command_end = output.find('\n')
            prompt_start = (len(output)-1) - output[::-1].find('\n')+1
            self.prompt = output[prompt_start:] #  what if there is /n check ??
            if command_end == prompt_start-1:
                return ''
            else:
                return output[command_end+1:prompt_start]
        else: 
            return ''
        

    def auth(self):
        if not self.connected:
            raise Exception('Authentication is not possible if not connected')
        if self.protocol == 'tel':
            logging.debug(f'    TELNET AUTH WILL BE STARTED: ({self.host}:{self.port}) username = {self.username}')
            self.auth_tel()
        elif self.protocol == 'ssh':
            raise Exception('Base_class - auth for ssh not implemented yet')


    def auth_tel(self):
        logging.debug(f'  TELNET AUTHENTICATION STARTED: ({self.host}:{self.port}) username = {self.username}')
        _, _, output = self.connection.expect([self.rLOGINPROMPT], self.global_timeout)
        self.banner = output.replace(b'\r\n', b'\n').decode('utf-8', 'ignore')
        logging.debug(f'    TELNET AUTH USERNAME PROMPT: ({self.host}:{self.port}) banner+username prompt:\n{self.banner}')
        logging.debug(f'   TELNET AUTH SENDING USERNAME: ({self.host}:{self.port}) username = {self.username}')
        self.connection.write(self.username + tENTER)
        logging.debug(f'      TELNET AUTH USERNAME SENT: ({self.host}:{self.port}) username = {self.username}')
        _, m, output = self.connection.expect([self.rPASSPROMPT], self.global_timeout)
        logging.debug(f'    TELNET AUTH PASSWORD PROMPT: ({self.host}:{self.port}) username+password prompt:\n{output}')
        logging.debug(f'   TELNET AUTH SENDING PASSWORD: ({self.host}:{self.port})')
        self.connection.write(self.password + tENTER)
        logging.debug(f'      TELNET AUTH PASSWORD SENT: ({self.host}:{self.port})')
        self.post_auth_check()


    def post_auth_check(self): 
        logging.debug(f'     POST AUTH CHECKING STARTED: ({self.host}:{self.port})')
        if not self.rAUTHFAIL:
            raise Exception('rAUTHFAIL not defined in subclass')
        logging.debug(f' WAITING FOR PROMPT/FAILURE MSG: ({self.host}:{self.port}), self.global_timeout = {self.global_timeout}')
        _, match, output = self.connection.expect([self.rPROMPT, self.rAUTHFAIL], self.global_timeout)
        outputdecoded = output.decode('utf-8', 'ignore')
        logging.debug(f'         GOT PROMPT/FAILURE MSG: ({self.host}:{self.port}) got:\n{outputdecoded}')
        if not match:
            self.authenticated = False
            raise AuthException('Authentication failed, nothing matched')

        if 'prompt' in match.groupdict():
            self.authenticated = True
            self.promptsign = match.groupdict()['promptsign'].decode('utf-8', 'ignore')
            self.prompt = match.groupdict()['prompt'].decode('utf-8', 'ignore') + self.promptsign
        elif 'failmessage' in match.groupdict():
            self.authenticated = False
            output = output.decode('utf-8', 'ignore')
            raise AuthException(f'Authentication failed,  fail message:\n{output}')


    def disconnect(self):
        logging.debug(f'                  DISCONNECTING: ({self.host}:{self.port})')
        if self.connected:
            self.connection.close()


    def get_mactable(self):
        Iam = type(self).__name__
        raise NotImplementedError(f'for {Iam} this method is not implemented')


    def get_intftable(self):
        Iam = type(self).__name__
        raise NotImplementedError(f'for {Iam} this method is not implemented')

    def get_ipintftable(self):
        Iam = type(self).__name__
        raise NotImplementedError(f'for {Iam} this method is not implemented')

    def get_intfullinfo(self):        
        Iam = type(self).__name__
        raise NotImplementedError(f'for {Iam} this method is not implemented')

    def get_arptable(self):
        Iam = type(self).__name__
        raise NotImplementedError(f'for {Iam} this method is not implemented')

    def get_routingtable(self):
        Iam = type(self).__name__
        raise NotImplementedError(f'for {Iam} this method is not implemented')

