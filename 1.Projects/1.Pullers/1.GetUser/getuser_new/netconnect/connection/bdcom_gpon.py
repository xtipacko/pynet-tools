from netconnect.connection.ciscolike import *
from netconnect.connection.classification import ciscolike_modes

class BDCom_GPON(Ciscolike):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def auth_tel(self):
        super().auth_tel()
        if self.authenticated:
            #reduce doubleprompt for bdcoms
            self.connection.expect([self.rPROMPT], self.global_timeout)
