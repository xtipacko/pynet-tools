from netconnect.connection.ciscolike import Ciscolike
from netconnect.connection.classification import ciscolike_modes
from netconnect.nettypes import VlanRange, MacAddress, MacEntry
from netconnect.nettypes import MacTable, ArpEntry, ArpTable
from netconnect.nettypes import InterfaceName, InterfaceEntry
from netconnect.nettypes import InterfaceTable, RouteEntry, RouteTable
import re

rSWITCHPORT = r'(?P<intf>.*)\n[\s\S]*Operational\ Mode:\ (?P<mode>.*)\n'


intstate_map =  { 'connected'   : 'up',
                  'notconnect'  : 'down',
                  'disabled'    : 'admin-down',
                  'err-disabled': 'err-disabled'}

class Cisco3750like(Ciscolike):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    

    def get_mactable(self):
        texttable = self.send_command('show mac address-table dynamic')
        # starting from line 5 we have mac addresses, 
        # last line show total number of mac addresses
        texttable = texttable.splitlines()[5:-1]
        mactable = MacTable()
        for entry in texttable:
            vlan, mac, intf = entry[0:4].lstrip(), entry[8:22], entry[38:].rstrip()
            mactable.append(mac, intf, vlan)
        return mactable
                

    def get_intftable(self):
        texttable = self.send_command('show interface status')
        # starting from line 2 we have list of interfaces
        texttable = texttable.splitlines()[2:]
        intftable = InterfaceTable()
        for entry in texttable:
            interface = entry[:10].rstrip()
            intfentry = InterfaceEntry(interface, 
                                       description = entry[10:29].rstrip(),
                                       state       = intstate_map.get(entry[29:42].rstrip(), 'unknown'),
                                       accessvlan  = entry[42:53].rstrip(),
                                       duplex      = entry[53:59].lstrip(),
                                       speed       = entry[59:66].lstrip(),
                                       intftype    = entry[67:].rstrip())

            intftable.append(intfentry)
        return intftable


    def get_intffullinfo(self):        
        intftable = self.get_intftable()
        texttable = self.send_command('show interface switchport')
        texttable = texttable.split('Name: ')[1:]
        for entry in texttable:
            

        


    def get_ipintftable(self):
        pass


    def get_arptable(self):
        pass

    def get_routingtable(self):
        pass


    

    def disconnect(self):
        self.send_command('logout')
        super().disconnect()
