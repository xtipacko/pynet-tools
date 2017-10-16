from telnetlib import Telnet

PROMPT = [r'\n.*[#>]'.encode('ascii', 'ignore')]
LOGINPROMPT = [r'Username:\ '.encode('ascii', 'ignore')]
PASSWORDPROMPT = [r'Password:\ '.encode('ascii', 'ignore')]
ENTER = b'\r\n'

class ConnectHandler:

    def __init__(self, **kwargs):
        self.device_type = kwargs['device_type']
        self.ip          = kwargs['ip']
        self.username    = kwargs['username'].encode('ascii', 'ignore')
        self.password    = kwargs['password'].encode('ascii', 'ignore')
        self.connection  = Telnet(self.ip, 23)
        self.auth()


    def normalise_output(self, strval):
        return '\n'.join((strval.replace(b'\r\n', b'\n').decode('utf-8', 'ignore').splitlines())[1:-1])        


    def auth(self):
        self.connection.expect(LOGINPROMPT, 2)
        self.connection.write(self.username + ENTER)
        self.connection.expect(PASSWORDPROMPT, 2)
        self.connection.write(self.password + ENTER)
        self.connection.expect(PROMPT, 2)


    def send_command(self, command):
        self.connection.write(command.encode('ascii', 'ignore') + ENTER)
        _, _, output = self.connection.expect(PROMPT, 2)
        return self.normalise_output(output)   


    def disconnect(self):
        self.connection.close()


    def enable(self):
        pass
        #no need

