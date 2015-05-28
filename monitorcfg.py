#!/usr/bin/env python

import textfsm
import connect
from connect import *
import logging



def txt_fsm_parser(inputf, templatef):
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

def prefix_to_nh(arg_dict):
    """
    Match a specific next-hop for a given route from the routing table
    """
    prefix = arg_dict['prefix']
    ip = arg_dict['ip']
    fsmresult = arg_dict['fsmresult']

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

def ios_int_up(arg_dict):
    """
    IOS: show ip int brief: Is an interface UP?
    """
    interface = arg_dict['interface']
    fsmresult = arg_dict['fsmresult']

    isResult = False
    for row in fsmresult:
        #print row
        if row[0] == interface and row[4] == 'up' and row[5] == 'up':
            isResult = True
    return isResult


def ios_int_ip(arg_dict):
    """
    IOS: show ip int brief: Is the interface configured with this IP
    """
    interface = arg_dict['interface']
    ip = arg_dict['ip']
    fsmresult = arg_dict['fsmresult']

    isResult = False
    for row in fsmresult:
        #print row
        if row[0] == interface and row[1] == ip:
            isResult = True
    return isResult


def ios_rib_size(arg_dict):
    """
    IOS: get the number of prefixes in the RIB
    """
    fsmresult = arg_dict['fsmresult']
    result = 0
    for row in fsmresult:
        print row
        if row[0] == 'Total ':
            result = row[1]
    return result


def ios_isprefix_prot(arg_dict):

    prefix = arg_dict['prefix']
    code = arg_dict['code']
    fsmresult = arg_dict['fsmresult']

    result = False
    for row in fsmresult:
        #print row
        if row[0] == code and row[1] == prefix:
            result = True
            #print row
    return result

def ios_isprefix(arg_dict):

    prefix = arg_dict['prefix']
    fsmresult = arg_dict['fsmresult']

    result = False
    for row in fsmresult:
        #print row
        if row[1] == prefix:
            result = True
            #print row
    return result


def ios_isprefix_nh(arg_dict):

    prefix = arg_dict['prefix']
    nh = arg_dict['nh']
    fsmresult = arg_dict['fsmresult']

    result = False
    for row in fsmresult:
        #print row
        if row[1] == prefix and row[4] == nh:
            result = True
            #print row
    return result



#OK
# single command : to include in the class InitDev
#f,c = para_ssh('192.168.0.207','sh cry ipsec sa', 'admin' ,'IOU7', '1', '1', '1', 'cisco')



# main program

# Get device data dictionary from a YAML FILE
#remote_dev(logger, readYaml('cmds.yaml'), flg=True, timeout=300)
#print remote_dev(logger, readYaml('cmds.yaml'), flg=True, timeout=300)



"""
# Get device data dictionary from a script Dictionary object
dataDict = {'R1': [\
    {'ip': '192.168.0.204'}, \
    {'login': 'admin'}, \
    {'password': 'cisco'}, \
    {'sleep': 0}, \
    'sh ip route | i 70.0.0.0 '
    ]}

output_file = remote_dev(logger, dataDict, flg=filelog, timeout=300) # command result file name
result = txt_fsm_parser(output_file[0], 'ios_isprefix_prot.templ')
print result
arg_dict = {}
arg_dict['prefix'] = '70.0.0.0'
arg_dict['nh'] = '172.16.70.7'
arg_dict['result'] = result
print ios_isprefix_nh(arg_dict)
"""


"""
# Examples
# fn: apply textfsm to (filename + template)
# get a list of lists
# fn: extract needed inf from list of lists & synthesize a boolean value

#1: is the nh for this prefix?
result = txt_fsm_parser('route.txt', 'route.temp')
print prefix_to_nh(result, '192.0.2.76/30', '203.0.113.183')

#2: is this ip for this interface?
result = txt_fsm_parser('get_interfaces.input', 'get_interfaces.temp')
print ios_int_up(result, 'Ethernet0/0')
print ios_int_ip(result, 'Ethernet0/0', '192.168.17.7')

######3 IOS: get RIB size (prefix number)
# Get device data dictionary from a script Dictionary object
dataDict = {'R1': [\
    {'ip': '192.168.0.204'}, \
    {'login': 'admin'}, \
    {'password': 'cisco'}, \
    {'sleep': 0}, \
    'sh ip route summary'
    ]}

output_file = remote_dev(logger, dataDict, flg=filelog, timeout=300) # command result file name
result = txt_fsm_parser(output_file[0], 'ios_prefix_size.templ')
print ios_rib_size(result)

######4 IOS: is the prefix learned from a specific routing protocol?
# Get device data dictionary from a script Dictionary object
dataDict = {'R1': [\
    {'ip': '192.168.0.204'}, \
    {'login': 'admin'}, \
    {'password': 'cisco'}, \
    {'sleep': 0}, \
    'sh ip route | i 70.0.0.0 '
    ]}

output_file = remote_dev(logger, dataDict, flg=filelog, timeout=300) # command result file name
result = txt_fsm_parser(output_file[0], 'ios_isprefix_prot.templ')
print result
print ios_isprefix_prot('D', '70.0.0.0', result)

######5 IOS: is the prefix in the RIB?
# Get device data dictionary from a script Dictionary object
dataDict = {'R1': [\
    {'ip': '192.168.0.204'}, \
    {'login': 'admin'}, \
    {'password': 'cisco'}, \
    {'sleep': 0}, \
    'sh ip route | i 70.0.0.0 '
    ]}

output_file = remote_dev(logger, dataDict, flg=filelog, timeout=300) # command result file name
result = txt_fsm_parser(output_file[0], 'ios_isprefix_prot.ios_isprefix_prot')
print result
print ios_isprefix('70.0.0.0', result)

######6 IOS: does a prefix has a specific nh?
# Get device data dictionary from a script Dictionary object
dataDict = {'R1': [\
    {'ip': '192.168.0.204'}, \
    {'login': 'admin'}, \
    {'password': 'cisco'}, \
    {'sleep': 0}, \
    'sh ip route | i 70.0.0.0 '
    ]}

output_file = remote_dev(logger, dataDict, flg=filelog, timeout=300) # command result file name
result = txt_fsm_parser(output_file[0], 'ios_isprefix_prot.templ')
print result
print ios_isprefix_nh('70.0.0.0','172.16.70.7', result)


"""