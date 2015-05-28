__author__ = 'AJ NOURI'
__date__ = ''
__license__ = ''
__version__ = ''
__email__ = 'ajn.bin@gmail.com'

#!/usr/bin/env python
from Tkinter import *
import tkMessageBox
from tkFileDialog import askopenfilename
import tkSimpleDialog
import ttk
import yaml
import monitorcfg
import logging
from connect import *
import connect

"""

TODO:
 - get the function (must match with predefined fns in monitorcfg.py)
 - call function monitorcfg module, get the state, rewrite column state & change the color

from monitorcfg import *

f = 'prefix_to_nh'

try:
 func = getattr(monitorcfg, f)
 except AttributeError:
     print ' missing method'
 else:
     result = func()

"""

def logg_fn(loglevel):

    logger = logging.getLogger(__name__)
    ### Manually set logging level
    #logging.basicConfig(level=logging.INFO)
    logging.basicConfig(level=loglevel)

    handler = logging.FileHandler('initconfig.log', mode='w')
    # Create logging format and bind to root logging object
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s')
    # Create file handler
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger




class TrackApp(Frame):
    # The class TrackApp inherits from the Frame container widget
    def __init__(self, parent):
        Frame.__init__(self, parent)

        # reference to the parent widget. The parent widget is the Tk root window
        self.parent = parent


        # **************** initialise the tree widget ans it columns
        # insert the tree into the bottomframe
        self.tree = ttk.Treeview(self.parent)
        self.tree["columns"] = ("state")

        self.tree.column("state", width=100)
        self.tree.heading("state", text="State")

        self.vsb = ttk.Scrollbar(self.parent, orient=VERTICAL, command=self.tree.yview)
        self.hsb = ttk.Scrollbar(self.parent, orient=HORIZONTAL, command=self.tree.xview)
        self.vsb.grid(row=1, column=1, sticky='ns')
        self.hsb.grid(row=2, column=0, sticky='ew')
        self.tree.configure(yscrollcommand=self.vsb.set)
        self.tree.configure(xscrollcommand=self.hsb.set)

        self.tree.grid(row=1, column=0, sticky=N + W + E + S)

        self.f = "outline2.yaml"

        self.read_param(monitorcfg, self.read_yaml(self.f))



    def doNothing(self):
        print("do something")


    def read_yaml(self, f):
        if f:
            stream = open(f)
            return yaml.load(stream)

        else:
            return []


    def read_param(self, fn_module, data):

        try:
            remote_dev = getattr(connect, 'remote_dev')
            txt_fsm_parser = getattr(fn_module, 'txt_fsm_parser')


        except AttributeError:
            print 'missing method from module', fn_module
        else:

            if data != []:
                for item in data:
                    #print '===>  ',item
                    #for key,value in item.items():
                    #    print key,': ',value

                    print item.get('description')
                    print item.get('function')
                    print item.get('args')
                    print item.get('device').get('hostname')
                    print item.get('device').get('ip')
                    print item.get('device').get('login')
                    print item.get('device').get('password')
                    print item.get('device').get('sleep')
                    print item.get('command')
                    print item.get('template')

                    # Constructing the data format used by remote_dev in connect module
                    # TODO: Change data format (Awkward!!) used by remote_dev in connect module

                    dataDict = {}
                    deviceList = []
                    ip = {}
                    login = {}
                    password = {}
                    sleep = {}
                    ip['ip'] = item.get('device').get('ip')
                    login['login'] = item.get('device').get('login')
                    password['password'] = item.get('device').get('password')
                    sleep['sleep'] = item.get('device').get('sleep')
                    dataDict[item.get('device').get('hostname')] = deviceList
                    deviceList.append(ip)
                    deviceList.append(login)
                    deviceList.append(password)
                    deviceList.append(sleep)
                    deviceList.append(item.get('command'))

                    # Get command output from the remote device
                    output_file = remote_dev(logg_fn(logging.DEBUG), dataDict, flg=True, timeout=300)

                    # Apply textFSM template to command output
                    result = txt_fsm_parser(output_file[0], item.get('template'))
                    print result

                    # Call the function to parse textFSM result
                    try:
                        func = getattr(fn_module, item.get('function'))
                    except AttributeError:
                        print 'missing method ',item.get('function'),' from module', fn_module
                    else:

                        #Prepare the dictionary of arguments
                        arg_dict = item.get('args')
                        arg_dict['fsmresult'] = result

                        print 'FINAL RESULT ===> ',func(arg_dict)

                        if  func(arg_dict):
                            backgrnd = 'green'
                        else:
                            backgrnd = 'red'

                    print backgrnd
                    id1 = self.tree.insert('', 0, text=item.get('description').strip('\r\n'), \
                                      values=("NOK","","","","",""),\
                                      tags=('state','','','','',''))

                    self.tree.tag_configure('state', background=backgrnd)

            else:
                print 'Empty yaml file'





def main():
    # create a root window
    root = Tk()
    app = TrackApp(root)
    MAINTITLE = "Config monitoring"
    root.wm_title(MAINTITLE)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(1, weight=3)
    root.wm_protocol("WM_DELETE_WINDOW", exit)  # does work

    logg_fn(logging.DEBUG)

    # Enter event loop
    root.mainloop()


if __name__ == "__main__":
    main()


"""
                id1 = self.tree.insert('' , 0,    text=key0.strip('\r\n'), \
                                  values=("10","","","","",""),\
                                  tags=('domaint','','','','',''))
                self.tree.tag_configure('domaint', background='yellow')
                self.tree.tag_bind('domaint', '<Button-3>', self.popupEntry)
"""