import csv
import os
from pprint import pprint

def extract_devlist(path='Devices.csv'):
    if not ('\\' in path or
            '/'  in path):
        scriptdir = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(scriptdir, path)
    try:
        with open(path, 'r') as devcsv:
            devlist = csv.DictReader(devcsv)
    except Exception as e:
        print(f'unknown exception opening:\n {path}\n {e}')


if __name__ == '__main__':
    extract_devlist()

