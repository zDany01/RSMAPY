import os
from os.path import exists, dirname, abspath
import logging

lg = logging.getLogger("uvicorn.RSMAPY")

def preBootCheck():
    try:
        import config
        lg.setLevel(logging.DEBUG if config.DEBUG_LOGGING else logging.INFO)
        lg.info("Configuration loaded correctly")
    except:
        print("You need to rename \"config.py.template\" to \"config.py\"" if exists(dirname(dirname(abspath(__file__))) + "/config.py.template") else "No configuration file found...\nExiting...")
        exit(1)

    notAdmin: bool
    try:
        notAdmin = os.getuid() != 0
    except AttributeError:
        print("This API can only be executed on Linux")
        exit(182)
    if notAdmin:
        lg.error("Make sure to execute this API with sudo priviledges")
        exit(1)