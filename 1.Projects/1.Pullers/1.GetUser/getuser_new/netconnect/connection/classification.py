device_types = { 'cisco-ISRlike',
                 'cisco-ASR-ios-xe',
                 'cisco-65xx.1',
                 'cisco-65xx.2',   # difference in command outputs
                 'cisco-49xx.1',   # check if it is ios or is it  IOS-XR...
                 'cisco-3750like', # ? 2950, 3550... 
                 'ciscolike',      #for future - class, which can understand any cisco device
                 'snr-type1',
                 'snr-type2',
                 'alpha',
                 'eltex-mes',
                 'eltex-ltp',
                 'dlink',
                 'bdcom',
                 'mikrotik',
                 'dlink-dir100',
                 'generic'   } 

con_protocols = { 'ssh', 'tel' }

device_roles = { 'l3', 'l2', 'router' }

ciscolike_modes = { 'initial', 
                    'user',
                    'priv', 
                    'config', 
                    'config-if',
                    'config-line',
                    'config-router'  }