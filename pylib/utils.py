import os
from os.path import exists, dirname, abspath


def preBootCheck(): 
    notAdmin: bool
    try:
        notAdmin = os.getuid() != 0
    except AttributeError:
        print("This API can only be executed on Linux")
        exit(182)
    if notAdmin:
        print("Make sure to execute this API with sudo priviledges")
        exit(1)
    
    try:
        import config
        print("Configuration loaded correctly")
    except:
        print("You need to rename \"config.py.template\" to \"config.py\"" if exists(dirname(dirname(abspath(__file__))) + "/config.py.template") else "No configuration file found...\nExiting...")
        exit(1)