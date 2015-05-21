#!/usr/bin/env python

import logging
import textfsm
from connect import *



def textFSMParser(inputf, templatef):
    """
    Open the template file, and initialise a new TextFSM object with it.
    :param inputf:
    :param templatef:
    :return:
    """
    fsm = textfsm.TextFSM(open(templatef))

    with open(inputf, "r") as inf:
      inputf = inf.read()
      fsm_results = fsm.ParseText(inputf)
      return fsm_results

####################################################################################################

def prefixToNH(fsmresult, prefix, ip):
    """
    Match a specific next-hop for a given route from the routing table
    :param fsmresult:
    :return:
    """
    #print fsmresult
    isResult = False
    for row in fsmresult:
        if row[2] == '192.0.2.76/30':
            #print row[2]
            #print row[3]
            for nh in row[3]:
                if nh == '203.0.113.183':
                    #print nh
                    isResult = True
    return isResult

def interfaceUP(fsmresult, interface):
    """
    IOS: show ip int brief: Is an interface UP?
    :param fsmresult:
    :param interface:
    :return:
    """
    isResult = False
    for row in fsmresult:
        #print row
        if row[0] == interface and row[4] == 'up' and row[5] == 'up':
            isResult = True
    return isResult


def interfaceIP(fsmresult, interface, ip):
    """
    IOS: show ip int brief: Is the interface configured with this IP
    :param fsmresult:
    :param interface:
    :param ip:
    :return:
    """
    isResult = False
    for row in fsmresult:
        #print row
        if row[0] == interface and row[1] == ip:
            isResult = True
    return isResult




#OK
# single command : to include in the class InitDev
#f,c = para_ssh('192.168.0.207','sh cry ipsec sa', 'admin' ,'IOU7', '1', '1', '1', 'cisco')



# main program

# Get device data dictionary from a YAML FILE
#remoteDev(logger, readYaml('cmds.yaml'), flg=True, timeout=300)
#print remoteDev(logger, readYaml('cmds.yaml'), flg=True, timeout=300)




logger = logging.getLogger(__name__)
### Manually set logging level
#logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.DEBUG)

handler = logging.FileHandler('initconfig.log', mode='w')
# Create logging format and bind to root logging object
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s')
# Create file handler
handler.setFormatter(formatter)
logger.addHandler(handler)
filelog = True





# Get device data dictionary from a script Dictionary object
dataDict = {'R1': [\
    {'ip': '192.168.0.207'}, \
    {'login': 'admin'}, \
    {'password': 'cisco'}, \
    {'sleep': 0}, \
    'sh ip route'
    ]}

print remoteDev(logger, dataDict, flg=filelog, timeout=300) # command result file name

# fn: apply textfsm to (filename + template)
# get a list of lists
# fn: extract needed inf from list of lists & synthesize a boolean value


result = textFSMParser('route.txt', 'route.temp')
print prefixToNH(result, '192.0.2.76/30', '203.0.113.183')

result = textFSMParser('get_interfaces.input', 'get_interfaces.temp')
print interfaceUP(result, 'Ethernet0/0')
print interfaceIP(result, 'Ethernet0/0', '192.168.17.7')