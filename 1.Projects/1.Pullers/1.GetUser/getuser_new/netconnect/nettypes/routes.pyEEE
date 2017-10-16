from . import *
from ipaddress import ip_network, ip_address

routetypes = {'connected', 
              'static', 
              'dynamic',
              ''}

routeprotocols = {'ospf', 
                  'ospf-ia', 
                  'ospf-external1', 
                  'ospf-external2', 
                  'ospf-ns-external1', 
                  'ospf-ns-external2', 
                  'eigrp',
                  'eigrp-external',
                  'bgp',
                  'nhrp',
                  '' }

class RouteEntry:
    def __init__(self, *args, **kwargs):
        ''' 
        RouteEntry(prefix, ln, nexthop, interface='', routetype='', routeprotocol='') 
         or
        RouteEntry(subnet, nexthop, interface='', routetype='', routeprotocol='') where subnet 'prefix/ln' '''
        #treat 3 args as prefix, length, nexthop
        #treat 2 args as prefix/ln, nexthop
        if len(args) == 3:
            prefix = args[0]
            ln = args[1]
            nexthop = args[2]
            self.subnet = ip_network(f'{prefix}/{ln}')
            self.nexthop = nexthop
        elif len(args) == 2:
            subnet  = args[0]
            nexthop = args[1]
            self.subnet = ip_network(subnet)
            self.nexthop = nexthop
        else:
            raise TypeError(f'{self.__name__} ({self.__class__}): can take either 2 args (subnet, nexthop) + kwargs or 3 args (prefix, ln, nexthop) + kwargs')
        
        self.interface  = kwargs.get('interface', '')

        if 'routetype' in kwargs and kwargs['routetype'] not in routetypes:
            raise TypeError(f'Routetype: {kwargs["routetype"]} is not allowed for {self.__class__}, use {routetypes}')
        self.routetype  = kwargs.get('routetype', '')

        if 'routeprotocol' in kwargs and kwargs['routeprotocol'] not in routeprotocols:
                raise TypeError(f'Routeprotocol: {kwargs["routeprotocol"]} is not allowed for {self.__class__}, use {routeprotocols}')
        self.routeprotocol  = kwargs.get('routeprotocol', '')      

        self.adistance  = kwargs.get('adistance', None)
        self.metric  = kwargs.get('metric', None)
    
    def __contains__(self, other):
        if type(other) == ip_address:
            return other in self.subnet
        if type(other) == str:
            return ip_address(other) in self.subnet


class RouteTable(list):
 
    def filter(self, **kwargs):
        result = RouteTable()

        if 'routetype' in kwargs and kwargs['routetype'] not in routetypes: 
            raise TypeError(f'allowed only: {routetypes} routetype values')
        if 'routeprotocol' in kwargs and kwargs['routeprotocol'] not in routeprotocols: 
            raise TypeError(f'allowed only: {routeprotocols} routeprotocol values')

        

        for route in self:
            conditions = [ 'routetype'     not in kwargs or route.routetype     == kwargs['routetype'],
                           'routeprotocol' not in kwargs or route.routeprotocol == kwargs['routeprotocol'],
                           'interface'     not in kwargs or route.interface     == kwargs['interface'],
                           'nexthop'       not in kwargs or route.nexthop       == kwargs['nexthop'],
                           'subnet'        not in kwargs or route.subnet        == kwargs['subnet'],
                           'adistance'     not in kwargs or route.adistance     == kwargs['adistance'],
                           'metric'        not in kwargs or route.metric        == kwargs['metric'] ]
            if all(conditions):
                result.append(route)


        return result


    def lookup_subnet(self, network, longer_prefixes):

        def is_binnetwork_in_route(binnetaddr, route, routeprefixln, netwprefixln):
            route_bin_subnetaddr = int.from_bytes(route.subnet.network_address.packed, byteorder='big')            
            rsaddr = route_bin_subnetaddr   >> (32-routeprefixln) # shifted (sub)network address for each route
            nsaddr = binnetaddr >> (32-routeprefixln)
            return rsaddr == nsaddr and netwprefixln >= routeprefixln # if network addresses for route in list and given network match

        def is_route_in_network(binnetaddr, route, routeprefixln, netwprefixln):
            route_bin_subnetaddr = int.from_bytes(route.subnet.network_address.packed, byteorder='big')            
            rsaddr = route_bin_subnetaddr   >> (32-netwprefixln) # shifted (sub)network address for each route
            nsaddr = binnetaddr >> (32-netwprefixln)
            return rsaddr == nsaddr and netwprefixln <= routeprefixln # if network addresses for route in list and given network match
        
        binnetaddr = int.from_bytes(network.network_address.packed, byteorder='big')
        netwprefixln = network.prefixlen
        routes = RouteTable()

        if longer_prefixes:
            for route in self:
                routeprefixln = route.subnet.prefixlen # prefix length for each route   
                if is_route_in_network(binnetaddr, route, routeprefixln, netwprefixln):
                    routes.append(route)
            return routes
        else:
            logestmatch_prefixln = 0
            for route in self:
                routeprefixln = route.subnet.prefixlen # prefix length for each route                
                if is_binnetwork_in_route(binnetaddr, route, routeprefixln, netwprefixln):
                    if routeprefixln > logestmatch_prefixln:
                        logestmatch_prefixln = routeprefixln
                        routes = RouteTable()
                        routes.append(route)
                    elif routeprefixln == logestmatch_prefixln: 
                        routes.append(route)

            return routes


    def lookup_ip(self, ip):
        routes = RouteTable()
        logestmatch_prefixln = 0
        for route in self:            
            if ip_address(ip) in route.subnet:
                prefixln = route.subnet.prefixlen
                if prefixln > logestmatch_prefixln:
                    logestmatch_prefixln = prefixln
                    routes = RouteTable()
                    routes.append(route)
                elif prefixln == logestmatch_prefixln:
                    routes.append(route)

        return routes


    def lookup(self, *args, longer_prefixes=False):
        
        def lookuperror():
            raise Exception(f'{self.__name__} ({self.__class__}): can take either 1 (ip_network|ip_address|str ip|str network)\n or 2 arguments (str prefix,str ln), and 1 kwarg longer_prefixes (for networks only) ')
        
        if len(args) == 1:
            if type(args[0]) ==  ip_network:
                subnet = args[0]
                return self.lookup_subnet(subnet, longer_prefixes)
            elif type(args[0]) ==  str:
                if '/' in args[0]:
                    strsubnet = args[0]
                    return self.lookup_subnet(ip_network(strsubnet), longer_prefixes)
                elif '\\' in  args[0]:
                    prefix, ln = args[0].split('\\')
                    return self.lookup_subnet(ip_network(f'{prefix}/{ln}'), longer_prefixes)
                else:
                    if longer_prefixes:
                        lookuperror()
                    ip = args[0]
                    return self.lookup_ip(ip_address(ip))
            elif type(args[0]) ==  ip_address:
                if longer_prefixes:
                    lookuperror()
                return self.lookup_ip(ip)
            else:
                lookuperror()
        elif len(args) == 2:
            if type(args[0]) == str and type(args[1]) == str:
                prefix, ln = args
                self.lookup_subnet(ip_network(f'{prefix}/{ln}'), longer_prefixes)
            else:
                lookuperror()
        else:
            lookuperror()




#if __name__ == '__main__':
#    debug = False
#    routelist = RouteTable( [ RouteEntry('10.10.1.0', '24', 'where_was_ip', interface='Vlan11', routetype = 'connected'),
#                              RouteEntry('10.10.2.0', '24', 'where_was_ip', interface='Vlan12', routetype = 'static'),
#                              RouteEntry('10.10.3.0', '24', 'where_was_ip', interface='Vlan13', routetype = 'connected'),
#                              RouteEntry('10.10.4.0', '24', 'where_was_ip', interface='Vlan14', routetype = 'static'),
#                              RouteEntry('10.10.5.0', '24', 'where_was_ip', interface='Vlan15', routetype = 'connected'),
#                              RouteEntry('10.10.6.0', '24', 'where_was_ip', interface='Vlan16', routetype = 'static'),
#                              RouteEntry('10.10.7.0', '24', 'where_was_ip', interface='Vlan17', routetype = 'connected'),
#                              RouteEntry('10.10.0.0', '21', 'where_was_ip',interface='Vlan11', routetype = 'dynamic')] )
#
#    print([route.nexthop for route in routelist.lookup('10.10.0.0/21', longer_prefixes=True).filter(routetype = 'static', interface='Vlan15')])
    



