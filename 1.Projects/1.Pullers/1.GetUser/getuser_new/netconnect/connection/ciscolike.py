from netconnect.connection.base import *
from netconnect.connection.classification import ciscolike_modes



class Ciscolike(Connection):
    def __init__(self, *args, **kwargs):
        self.__allowedmodes = ciscolike_modes
        self.__prompt_to_mode_map = [ ('(config-if)', 'config-if'),
                                      ('(config)', 'config'),
                                      ('#', '>')
                                    ]
        self.enable_password = kwargs.get('enable_password', '')
        self.auto_enable = kwargs.get('auto_enable', True)
        self.__mode = 'initial'# ?? or after init , TO-DO: FIX PROBLEM IF IT IS BEFORE super.init, auto_enable doesn't work, if it is after super.init, can'not disable autoenable
        self.__prompt = None# ?? or after init
        super().__init__(*args, **kwargs)        


    def connect(self):
        super().connect()
        if self.auto_enable and self.mode == 'user':
            self.enable()
        self.adjustterminal()


    def adjustterminal(self):
        self.send_command('terminal length 0')
        # overwrite if needed


    def enable(self, force=False):
        if self.mode == 'user' or force:
            self.send_command('enable', expect=self.rENABLEPROMPT)
            output = self.send_command(self.enable_password)
        # to-do: if output shows fail, raise exception
    

    @property
    def mode(self):
        return self.__mode
    
    @mode.setter
    def mode(self, mode):
        if mode not in self.__allowedmodes:
            raise ValueError(f'mode: {mode} is unacceptable, use: {self.__allowedmodes}')
        else:
            self.__mode = mode


    @property
    def prompt(self):
        return self.__prompt
    
    @prompt.setter
    def prompt(self, prompt):
        logging.debug(f'def prompt(self, prompt):   prompt = {prompt}')
        if not prompt:
            self.mode = 'initial'
            return
        self.promptsign = prompt.rstrip()[-1]
        # can do better (with smth like dictionary f.e.):
        # more specific to the top
        if '(config-if)' in prompt:
            self.mode = 'config-if'

        elif '(config)'  in prompt:
            self.mode = 'config'

        elif '#'         in prompt:
            self.mode = 'priv'

        elif '>'         in prompt:
            self.mode = 'user'
 
        self.__prompt = prompt
        logging.debug(f'def prompt(self, prompt):   self.__prompt={self.__prompt}, self.promptsign={self.promptsign}, self.mode={self.mode},')



