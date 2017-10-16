from netconnect.nettypes.vlanrange import VlanRange
from netconnect.nettypes.maps import intreplacementmap
interfaceroles  = {'uplink', 'downlink', 'access'}
interfacestates = {'up', 'down', 'admin-down', 'err-disabled', 'unknown', ''}
interfacemodes  = {'access', 'trunk', 'qinq', 'unknown', ''}

class InterfaceName(str): #makes possible to compare interfaces by names
    def __eq__(self, other):
        return self.shorten(self) == self.shorten(other) 
    

    def shorten(self, intf):
        intf = intf.lower()
        for item in intreplacementmap:
            intf = intf.replace(*item)
        return intf


    @property
    def shortformat(self):
        return self.shorten(self)


class InterfaceEntry: #preferrably to use full notation
    def __init__(self, interface, **kwargs):
        self.interface       = InterfaceName(interface)
        self.description     = kwargs.get('description','')
        if 'accessvlan' in kwargs:
            if not kwargs['accessvlan'].isdigit() or int(kwargs['accessvlan']) > 4094:
                self.accessvlan = 'unknown'
            self.accessvlan      = kwargs['accessvlan']
        else:
            self.accessvlan = 'unknown'
        self.trunkvlans      = VlanRange(kwargs.get('trunkvlans', ''))
        self.nativevlan      = kwargs.get('nativevlan', 'unknown')
        self.duplex          = kwargs.get('duplex', '')
        self.speed           = kwargs.get('speed', '')
        self.intftype        = kwargs.get('intftype', '') # f.e. 10/100BaseTX

        if 'mode' in kwargs:
            if kwargs['mode'] not in interfacemodes:
                raise TypeError(f'Mode of interface: {kwargs["mode"]} is not allowed for interface, use {interfacemodes}')
            self.mode = kwargs.get('mode', 'unknown')

        if 'state' in kwargs:
            if kwargs['state'] not in interfacestates:
                raise TypeError(f'State of interface: {kwargs["state"]} is not allowed for interface, use {interfacestates}')
        self.state  = kwargs.get('state', 'unknown')

        if 'role' in kwargs:
            if kwargs['role'] not in interfaceroles:
                raise TypeError(f'Role: {kwargs["state"]} is not allowed for interface, use {interfaceroles}')
        self.role  = kwargs.get('role', 'access')

        if 'neighbour_device' in kwargs:
            if type(kwargs['neighbour_device']) == DeviceEntry:
                raise TypeError('neighbour_device attribute shold be instance of DeviceEntry class')
        self.neighbour_device  = kwargs.get('neighbour_device', None)
    

    def __str__(self):
        return self.interface



class InterfaceTable(dict): #interface is a key attribute
    def __setitem__(self, key, item): 
        self.__dict__[InterfaceName(key).shortformat] = item

    def __getitem__(self, key): 
        return self.__dict__[key]

    def __repr__(self): 
        return repr(self.__dict__)

    def __len__(self): 
        return len(self.__dict__)

    def __delitem__(self, key): 
        del self.__dict__[key]

    def clear(self):
        return self.__dict__.clear()

    def copy(self):
        return self.__dict__.copy()

    def has_key(self, k):
        return self.__dict__.has_key(k)

    def pop(self, k, d=None):
        return self.__dict__.pop(k, d)

    def update(self, *args, **kwargs):
        return self.__dict__.update(*args, **kwargs)

    def keys(self):
        return self.__dict__.keys()

    def values(self):
        return self.__dict__.values()

    def items(self):
        return self.__dict__.items()

    def pop(self, *args):
        return self.__dict__.pop(*args)

    def __cmp__(self, dict):
        return cmp(self.__dict__, dict)

    def __contains__(self, item):
        return item in self.__dict__

    def __iter__(self):
        return iter(self.__dict__)

    def __unicode__(self):
        return unicode(repr(self.__dict__))

    def search_by_role(self, role):
        if role not in interfaceroles:
            raise TypeError(f'Role: {kwargs["state"]} is not allowed for interface, use {interfaceroles}')
        result = InterfaceTable()
        for val in self.__dict__.values():
            if val.role == role:
                result.append(val)
        return result


    def search_by_vlan(self, vlan):
        result = InterfaceTable()
        for val in self.__dict__.values():
            if any( str(vlan) == str(val.accessvlan),
                    vlan in val.trunkvlans,
                    str(vlan) == str(val.nativevlan)):                
                result.append(val)
        return result


    def append(self, *args, **kwargs):
        if len(args) == 1 and len(kwargs) == 0:
            self[args[0].interface] = args[0]
        elif len(args) == 1 and len(kwargs) > 0:
            self[args[0]] = InterfaceEntry(args[0], **kwargs)
        else:
            raise TypeError(f'{self.__name__} ({self.__class__}): can take either 1 argument or 1 argument + several keyword arguments')
    