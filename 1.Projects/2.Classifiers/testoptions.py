import telnetlib
from time import sleep

def testcallback(sock, cmd, opt):
    if cmd == telnetlib.DO and opt == telnetlib.TTYPE:
        sock.sendall(b'\xff\xfb\x1f\xff\xfb\x20\xff\xfb\x18\xff\xfb\x27\xff\xfd\x01\xff\xfb\x03\xff\xfd\x03')
        sleep(.01)
        sock.sendall(b'\xff\xfa\x18\x00\x58\x54\x45\x52\x4d\xff\xf0')
        sleep(.01)
        sock.sendall(b'\xff\xfb\x24')


def trying():
    con.debuglevel = 1
    con.option_callback = callback

    sleep(3)
    #con.write(telnetlib.IAC + )
    print(con.read_very_eager())
    input('press any  key')

trying()