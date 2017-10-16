from . import *


class ArpEntry:
    def __init__(self, ip, mac, interface, age, vlan=None, static=False):
        self.ip = ip
        self.mac = MacAddress(mac)
        self.interface = InterfaceName(interface)
        self.age = age
        self.static = static
        if str(interface).startswith('Vlan'):
            self.vlan = interface[4:]
        elif vlan:
            self.vlan = vlan
    def __str__(self):
        return self.ip


class ArpTable(dict):    #ip is a key attribute
    def __setitem__(self, key, item): 
        self.__dict__[key] = item

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


    def search_by_mac(self, mac): #to-do: make it a  generator
        result = ArpTable()
        for val in self.__dict__.values():
            if MacAddress(val.mac) == MacAddress(mac):
                result.append(val)
        return result


    def append(self, *args, **kwargs):
        if len(args) == 1:
            self.__dict__[args[0].ip] = args[0]
        elif len(args) == 4:
            self.__dict__[args[0]] = ArpEntry(*args, **kwargs)
        else:
            raise Exception(f'{self.__name__} ({self.__class__}): can take either 1 or 4 args, and up to 2 kwargs')


    def reduce(self):
        '''if arp table consists only of entries for one mac or for one ip, method reduces table to a single arp entry (returns first)'''
        return self.__dict__[0]
