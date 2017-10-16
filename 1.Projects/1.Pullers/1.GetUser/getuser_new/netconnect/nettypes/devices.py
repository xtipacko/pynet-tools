from . import *
from ipaddress import ip_address
from copy import deepcopy
devroles = { 'swl2', 'swl3', 'router', 'firewall', 'server', 'unknown' }
devstates = { 'up', 'down', 'unknown' }

class DeviceEntry:
    def __init__(self, ipaddress, hostname, dudehostname=None, macaddress=None, 
                       arp_table=None, routing_table=None, interfaces=None,
                       ip_aliases=None, mac_aliases=None, mac_table=None,
                       state='unknown', role='unknown', parentl3=None ):
        self.ipaddress = ipaddress
        self.hostname = hostname
        if macaddress:
            self.macaddress = MacAddress(macaddress)
        if role not in devroles:
            raise TypeError(f'{self.__name__} ({self.__class__}): doesn\'t take role: {role}, use: {devroles}' )
        if state not in devstates:
            raise TypeError(f'{self.__name__} ({self.__class__}): doesn\'t take role: {state}, use: {devstates}' )
        self.role = role
        self.dudehostname = dudehostname
        self.arp_table = arp_table
        self.routing_table = routing_table
        self.interfaces = interfaces
        self.ip_aliases = ip_aliases
        self.mac_aliases = mac_aliases
        self.mac_table = mac_table
        self.parentl3 = parentl3


    def int_to_maclookup(self, interface):
        '''returns mac address-table for interface list, each device contains matched mac address'''
        #more actual for online lookups
        return self.mac_table.search_by_interface(interface)

    def mac_to_intlookup(self, mac, introlefilter=None):
        '''returns matched interface or None'''
        if mac not in self.mac_table:
            return None

        mac_entry = self.mac_table[MacAddress(mac).commonformat]
        if not self.interfaces or mac_entry.interface not in self.interfaces:
            raise Exception('mac_to_intlookup: no interface table or interface not in self.interfaces table')

        foundinterface = self.interfaces[mac_entry.interface]        
        if introlefilter:
            if introlefilter not in interfaceroles:
                raise TypeError(f'{self.__name__} ({self.__class__}): doesn\'t take role: {introlefilter}, use: {interfaceroles}' )
            if foundinterface.role == introlefilter:
                return mac_entry
            else:
                return None
        else:
            return mac_entry

    def arpiplookup(self, mac):
        '''returns new arptable filtered by mac address'''
        return self.arp_table.search_by_mac(mac)

    def arpmaclookup(self, ip):
        '''returns new arptable filtered by ip address (only one item is inside)'''
        arp_entry = self.arp_table[ip]
        arpfiltered = ArpTable()
        arpfiltered.append(arp_entry)
        return arpfiltered

    def arplookup(self, mac_or_ip):
        '''returns new arptable filtered by mac or ip address (whatever is present)'''
        try:
            ip_address(mac_or_ip)
            #ip = True
            return arpmaclookup(mac_or_ip)
        except AddressValueError:
            #ip = False
            return arpiplookup(mac_or_ip)

    #ipaddress (access) key in dict
    #hostname  auxilary key  __  
    #macaddress (access) auxilary key __
    #mac-table
    #arp-table
    #routing-table
    #role L2/L3
    #parentL3 (for L2)
    #interfaces
    #ip_aliases
    #mac_aliases



class DeviceTable(dict) :
    #ipaddress (access) key in dict
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

    def globalroutelookup(self, subnet, filterdict=None, longer_prefixes=False):
        '''returns device list, each device contains matched routes'''
        result = DeviceTable()
        for dev in self:
            devroutingtable = dev.routing_table.lookup(subnet, longer_prefixes=longer_prefixes)
            if filterdict:
                devroutingtable = devroutingtable.filter(**filterdict)
            
            if len(devroutingtable) > 0:
                newdev = deepcopy(dev) # creating copy for dev
                newdev.routing_table = devroutingtable # assigning looked up and filtered routes
                result.append(newdev) # will it work ?
        
        if len(result) > 0:
            return result
        else:
            return None
            

    def globalmaclookup(self, mac, introlefilter=None):
        '''returns device list, each device contains filtered mac-address-table of matched interfaces (usually only one for each device)'''
        result = DeviceTable()
        for dev in self:            
            mac_entry = dev.mac_to_intlookup(mac, introlefilter=introlefilter)
            if mac_entry:
                newdev = deepcopy(dev)
                newdev.mac_table = MacTable()
                newdev.mac_table.append(mac_entry)
                result.append(newdev)            
        if len(result) > 0:
            return result
        else:
            return None
    def __isipaddr(self, mac_or_ip):
        try:
            ip_address(mac_or_ip)
            return True
        except AddressValueError:
            return False


    def globalarplookup(self, mac_or_ip):
        '''returns device list with new arptables filtered by mac or ip address (whatever is present)'''
        result = DeviceTable()
        isip = self.__isipaddr(mac_or_ip)
        if isip:
            ip = mac_or_ip
            for dev in self:                
                newarptable = dev.arpmaclookup(ip)
                if len(newarptable) > 0:
                    newdev = deepcopy(dev)
                    newdev.arp_table = newarptable
                    result.append(newdev)
        else:
            mac = mac_or_ip
            for dev in self:
                newarptable = dev.arpiplookup(mac)
                if len(newarptable) > 0:
                    newdev = deepcopy(dev)
                    newdev.arp_table = newarptable
                    result.append(newdev)

        if len(result) > 0:
            return result
        else:
            return None


    def globalarpresolve(self, ip):
        '''returns first mac for ip or None'''
        globalarp = self.globalarplookup(ip)
        if len(globalarp) < 0:
            return None
        list(globalarp.values())[0]


    def append(self, dev):
        key = str(dev.ipaddress)
        self.__dict__[key] = dev
