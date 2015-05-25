### Examples
# fn: apply textfsm to (filename + template)
# get a list of lists
# fn: extract needed inf from list of lists & synthesize a boolean value

##1: is the nh for this prefix?
```python
result = txt_fsm_parser('route.txt', 'route.temp')
print prefix_to_nh(result, '192.0.2.76/30', '203.0.113.183')
```
-----------------------
```
##2: is this ip for this interface?
result = txt_fsm_parser('get_interfaces.input', 'get_interfaces.temp')
print ios_int_up(result, 'Ethernet0/0')
print ios_int_ip(result, 'Ethernet0/0', '192.168.17.7')
```
-----------------------

###3 IOS: get RIB size (prefix number)
# Get device data dictionary from a script Dictionary object
```python
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
```
-----------------------

###4 IOS: is the prefix learned from a specific routing protocol?
# Get device data dictionary from a script Dictionary object
```
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
```
-----------------------

###5 IOS: is the prefix in the RIB?
# Get device data dictionary from a script Dictionary object
```python
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
print ios_isprefix('70.0.0.0', result)
```
-----------------------

###6 IOS: does a prefix has a specific nh?
# Get device data dictionary from a script Dictionary object
```
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
```
-----------------------