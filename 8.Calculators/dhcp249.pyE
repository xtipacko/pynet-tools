#!/usr/bin/env python

# Terminology
# DD - Destination Descriptor (rfc3442)
# nAddr - Network Address
# Compact Network Address - Address with excluded insignificant (zero) octets
# ClRoute - Classless route
# WARNING Python's integers are not 32 bit in size, may be better to use numpy or similar library

from colorama import init as initcolor
from colorama import Fore as CLR
import re
import argparse
import sys

def Hex_to_Int(hexval):
    return int(hexval, 16)

def Hex_to_Dec(hexval):
    return str(Hex_to_Int(hexval))

def Str_to_BinIP(ip):
    Octets = list(map(int, ip.split(".")))
    binIP = (Octets[0] << 24) + (Octets[1] << 16) + (Octets[2] << 8) + Octets[3]
    return binIP

def Dec_to_HexIP(ip):
    binIP = Str_to_BinIP(ip)
    return "%08x" %binIP

def Hex_to_DecIP(hexip):
    hexOctets = [ hexip[0:2], hexip[2:4], hexip[4:6], hexip[6:8] ]
    decOctets = list(map(Hex_to_Dec, hexOctets))
    return ".".join(decOctets)


def Subnet_to_nAddr(ip, prefixln):
    binIP = Str_to_BinIP(ip)
    binMask = 0xffffffff - (0xffffffff >> prefixln)
    binNetw = binIP & binMask
    return binNetw

def Calc_HexWidth(prefixln):
    return -(-prefixln // 8)*2

def Compact_nAddr(ip, prefixln):
    binNetw = Subnet_to_nAddr(ip, prefixln)
    # -(-a // b) - integer division rounding up 
    HexWidth = Calc_HexWidth(prefixln)
    return ("{:08x}".format(binNetw))[:HexWidth]

def Hex_DD(strDD):
    ip, prefixln = strDD.split("/")
    prefixln = int(prefixln)
    return "{:02x}{:s}".format(prefixln, Compact_nAddr(ip, prefixln)) 

def Hex_ClRoutes(strClRs):    
    ''' Converts Classless Routes from string to hex
            Format example: "wherewasip/21 10.10.10.1 wherewasip/21 10.10.10.1"  (rfc3442)
    '''    
    def Hex_ClRoute(strClR):
        strDD, nexthop = re.split(r"\s*", strClR)
        hexDD = Hex_DD(strDD)
        return "%s%s" %(hexDD,  Dec_to_HexIP(nexthop))
    strClR = re.findall(r"(?:\d{1,3}\.){3}\d{1,3}/\d{1,2}\s+(?:\d{1,3}\.){3}\d{1,3}", strClRs)
    return "".join(list(map(Hex_ClRoute, strClR)))

def Split_ByFour(strVal, splitter="."):
    ptr=3
    maxindex = len(strVal)-1
    splByFour  = []
    while ( ptr <= maxindex ): #replasable to until logic
        splByFour.append(strVal[ptr-3:ptr+1])
        ptr+=4
    if (ptr > maxindex) and (ptr < maxindex+4):
        splByFour.append(strVal[ptr-3:maxindex+1])
    return splitter.join(splByFour)

def Dec_ClRoutes(hexClRs):
    ''' Converts Classless Routes from string to hex
            Format example: "156debb80a0a0a01149e3a800a0a0a01"  (rfc3442)
             mask compact_network_address nexthop ...
              15           6debb8         0a0a0a01
    '''   
    def Dec_CLRoute(hexClR, prefixln, HexWidth):
        compacthex_nAddr = hexClR[2:2+HexWidth]
        if (len(compacthex_nAddr) != HexWidth):
            raise Exception("Incorrect hexadecimal compact network address length:  \"%s\"" %compacthex_nAddr)
        hex_nAddr = "{0:0<8}".format(compacthex_nAddr)
        dec_nAddr = Hex_to_DecIP(hex_nAddr)
        hexNexthop = hexClR[2+HexWidth:2+HexWidth+8]
        if (len(hexNexthop) != 8):
            raise Exception("Incorrect hexadecimal next hop length: \"%s\"" %hexNexthop)
        decNexthop = Hex_to_DecIP(hexNexthop)
        return "%s/%d" %(dec_nAddr, prefixln), decNexthop
    ptr = 0
    listDecRoutes = []
    while (ptr < len(hexClRs)):
        prefixln = Hex_to_Int(hexClRs[ptr:ptr+2])
        if (prefixln != 0):
            HexWidth = Calc_HexWidth(prefixln)
            ptrNextHexDD = ptr+2+HexWidth+8
            listDecRoutes.append(Dec_CLRoute(hexClRs[ptr:ptrNextHexDD], prefixln, HexWidth))
        else:
            ptrNextHexDD = ptr+2+8
            listDecRoutes.append(Dec_CLRoute(hexClRs[ptr:ptrNextHexDD], prefixln, 0))
        ptr = ptrNextHexDD
    return listDecRoutes

def main():
    initcolor()
    parser = argparse.ArgumentParser(description="Calculates DHCP Option 121/249.", conflict_handler='resolve', \
        formatter_class=argparse.RawDescriptionHelpFormatter, \
        epilog=f"""Examples:\n
          %(prog)s wherewasip/21 10.10.10.1 wherewasip/21 10.10.10.1
            Output: {CLR.YELLOW}156d.ebb8.0a0a.0a01.159e.3a80.0a0a.0a01{CLR.RESET}

          %(prog)s -r 156d.ebb8.0a0a.0a01.159e.3a80.0a0a.0a01
            Output: {CLR.YELLOW}Subnet                Next hop{CLR.RESET}
                    wherewasip/21      10.10.10.1
                    wherewasip/21       10.10.10.1

          %(prog)s -hf /home/xtipacko/routes.txt
            Output: {CLR.YELLOW}156debb80a0a0a01159e3a800a0a0a01{CLR.RESET}""" )
    parser.usage  = f"{CLR.GREEN}%(prog)s [[-r] | [-h]] {{ [-f <file>] | <route0... routeN> }}{CLR.RESET}"
    parser.add_argument('-f', '--file', help="Input filename", metavar="file", type=str )
    parser.add_argument('--help', help="Show this help message ", action="help")
    parser.add_argument('routes', help="Routes in format: \"network/mask nexthop\"", nargs="*" )
    # creating and eliminating incompatible options using argparse
    mode_Reverse_or_Hex = parser.add_mutually_exclusive_group()
    mode_Reverse_or_Hex.add_argument('-r', '--reverse', help="Reverse calculation from hex to decimal notation" ,action='store_true')
    mode_Reverse_or_Hex.add_argument('-h', '--hex', help="Output without \".\" splitters, just hex", action='store_true')
    args = parser.parse_args()
    # eliminating remaining incompatible options manually
    if (args.file and args.routes):
        raise parser.error("\"-f/--file\" argument is not compatible with \"routes\"")
    elif (not args.file  and not args.routes and args.hex):
        parser.print_help()
        sys.exit(0)
    elif (not args.file  and not args.routes):
        raise parser.error("You should specify either \"--file\" argument or \"routes\"")
    # retreiving list of routes
    if (not args.file and args.routes):
        routes = " ".join(args.routes)
    elif(args.file and not args.routes):
        try:
            file = open(args.file, "r")
            routes = "".join(file.readlines())
        except:
            sys.stderr.write("Sorry, can not open file or read list of routes")
            sys.exit("File reading Error")
        finally:
            file.close()
    #checking options
    if (not args.hex and not args.reverse):
        print(Split_ByFour(Hex_ClRoutes(routes)))
    elif (args.hex and not args.reverse):
        print(Hex_ClRoutes(routes))
    elif (args.reverse and not args.hex):
        if (routes[:2] == "0x"):
            hexroutes = routes[2:]
        hexroutes = re.sub(r'[^0-9a-f]', "", routes)
        try:
            listDecRoutes = Dec_ClRoutes(hexroutes)
            _subnet, _nexthop  = "Subnet", "Next hop"
            print(f"{_subnet:<22}{_nexthop:<19}")
            colorl = [CLR.CYAN, CLR.GREEN]
            for i, (subnet, nexthop) in enumerate(listDecRoutes):
                clr = colorl[i % 2]
                print("{}{:<22}{:<19}{}".format(clr, subnet, nexthop,CLR.RESET))
        except Exception as err:
            print("Exception: %s" %err)

        

if ( __name__ == "__main__"):
    main()