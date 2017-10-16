from netconnect.nettypes.interfaces import InterfaceName


class MacAddress(str):
    def __eq__(self, other):
        mac1 = self.replace('.', '').replace(':', '').replace('-', '')
        mac2 = other.replace('.', '').replace(':', '').replace('-', '')
        mac1, mac2 = mac1.lower(), mac2.lower()
        
        return mac1 == mac2

    @property
    def commonformat(self):
        return self.replace('.', '').replace(':', '').replace('-', '').lower()
    
    @property
    def ciscoformat(self):
        pass

    @property
    def colonformat(self):
        pass

    @property
    def snrformat(self):
        pass
    
    @property
    def qtechformat(self): 
        pass




class MacEntry:
    def __init__(self, mac, interface, vlan):
        self.mac = MacAddress(mac)
        self.interface = InterfaceName(interface)
        self.vlan = vlan
    def __str__(self):
        return self.mac


class MacTable(dict):    #mac is a key attribute
    def __setitem__(self, key, item): 
        k = MacAddress(key).commonformat
        self.__dict__[k] = item

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

    def __contains__(self, item): #not very cool approach, change it because it compares mac keys, not mac entries
        return MacAddress(item).commonformat in self.__dict__

        #old: 
        #for mac in self.__dict__:
        #    if MacAddress(item) == MacAddress(mac):
        #        return True
        #else:
        #    return False

    def __iter__(self):
        return iter(self.__dict__)

    def __unicode__(self):
        return unicode(repr(self.__dict__))
    
    
    def search_by_interface(self, interface): #to-do: make it generator
        result = MacTable()
        for val in self.__dict__.values():
            if InterfaceName(val.interface) == InterfaceName(interface):
                result.append(val)
        return result


    def append(self, *args):
        if len(args) == 1:
            self[args[0].mac] = args[0]
        elif len(args) == 3:
            self[args[0]] = MacEntry(*args)
        else:
            raise Exception(f'{self.__name__} ({self.__class__}): can take either 1 or 3 arguments')
