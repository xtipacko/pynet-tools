import sys
import pyperclip
from colorama import Fore
from colorama import init as initcolor

pipeN = int(sys.argv[1]) % 65536
pyperclip.copy(str(pipeN))
initcolor()
print('New pipe number:',Fore.MAGENTA, f'{pipeN:}', Fore.RESET)
print('Copied to clip buffer')
