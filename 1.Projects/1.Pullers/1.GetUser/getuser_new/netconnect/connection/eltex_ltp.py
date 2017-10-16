from netconnect.connection.ciscolike import *
from netconnect.connection.classification import ciscolike_modes


class Eltex_LTP(Ciscolike):
    def __init__(self, *args, **kwargs):

        auto_connect = kwargs.get('auto_connect', True )

        kwargs['auto_connect'] = False
        super().__init__(*args, **kwargs)

        if self.global_timeout < 8: 
            self.global_timeout = 8

        if auto_connect:
            logging.debug(f'             AUTO CONNECTION TO: ({self.host}:{self.port})')
            self.connect()
    
    def adjustterminal(self):
    	pass

    def disconnect(self):
    	self.send_command('exit')
    	super().disconnect()
