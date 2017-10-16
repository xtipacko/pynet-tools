import csv
import os
from pprint import pprint
from copy import copy

def dictreader_to_dict(devlist):
    '''IP Addresses as keys'''
    #normalises dict by ip's:
    sep = ', '
    netwdevs = { dev['Addresses'].split(sep)[0]:{ 'dude_name'  : dev['Name'],
                                                  'dude_iplist': dev['Addresses'].split(sep) } 
                                                  for dev in devlist }
    return netwdevs

def extract_devlist(path='Devices.csv'):
    if not ('\\' in path or
            '/'  in path):
        scriptdir = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(scriptdir, path)
    try:
        with open(path, 'r') as devcsv:
            devlist = csv.DictReader(devcsv)
            return dictreader_to_dict(devlist)
    except Exception as e:
        print(f'unknown exception opening:\n {path}\n {e}')


if __name__ == '__main__':
    #pprint(extract_devlist())
    netwdevs = extract_devlist()

    show = [ '{dev:<20}{name:<48}{iplist!s:<32}'.format( dev    = dev,
                                                       name   = netwdevs[dev]["dude_name"],
                                                       iplist = netwdevs[dev]["dude_iplist"] ) 
             for dev in netwdevs ]
    show.insert(0, '{:<20}{:<48}{:<32}'.format('-IP ADDRESS-', '-DUDE\'s NAME-', '-IP ADDRESS LIST-'))
    print('\n'.join(show))
