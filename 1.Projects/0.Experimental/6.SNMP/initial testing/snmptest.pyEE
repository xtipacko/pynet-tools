from pysnmp.entity import engine, config
from pysnmp.carrier.asyncore.dgram import udp
from pysnmp.entity.rfc3413 import cmdgen
from pysnmp.proto import rfc1902
# Create SNMP engine instance
snmpEngine = engine.SnmpEngine()

#
# SNMPv3/USM setup
#

# user: usr-md5-none, auth: MD5, priv: NONE
config.addV3User(
    snmpEngine, 'there_was_snmpv3username',
    config.usmHMACMD5AuthProtocol, 'MazafakaRO'
)
config.addTargetParams(snmpEngine, 'my-creds', 'there_was_snmpv3username', 'authNoPriv')

#
# Setup transport endpoint and bind it with security settings yielding
# a target name
#

# UDP/IPv4
config.addTransport(
    snmpEngine,
    udp.domainName,
    udp.UdpSocketTransport().openClientMode()
)
config.addTargetAddr(
    snmpEngine, 'my-router',
    udp.domainName, ('10.10.10.1', 161),
    'my-creds'
)


# Error/response receiver
# noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal
def cbFun(snmpEngine, sendRequestHandle, errorIndication,
          errorStatus, errorIndex, varBinds, cbCtx):
    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        for oid, val in varBinds:
            print('%s = %s' % (oid.prettyPrint(), val.prettyPrint()))


# Prepare and send a request message, pass custom ContextEngineId & ContextName
cmdgen.GetCommandGenerator().sendVarBinds(
    snmpEngine,
    'my-router',
    # contextEngineId
    rfc1902.OctetString(hexValue='80003a8c04'),
    # contextName
    rfc1902.OctetString(''),
    [((1, 3, 6, 1, 2, 1, 1, 1, 0), None)],
    cbFun
)

# Run I/O dispatcher which would send pending queries and process responses
snmpEngine.transportDispatcher.runDispatcher()

