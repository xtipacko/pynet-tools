import os    
scriptdir = os.path.dirname(os.path.realpath(__file__))
with open(scriptdir + '\\passfile', 'r') as passfile:
    password = passfile.read()
    passfile.close()