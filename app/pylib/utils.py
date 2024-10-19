import os
from os.path import exists, dirname, abspath
import logging
from models import DockerAction, DockerList

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

def DockerResponse(action: str, affectedList: list[str], totalCount: int, invalidList: list[str] = None) -> DockerAction:
    response: DockerAction
    affected: int = len(affectedList)
    if(affected == 0):
        response = DockerAction(action=action, result= "None")
    elif (affected == totalCount):
        response = DockerAction(action=action, result="Valid" if invalidList else "Ok")
    else:
        response = DockerAction(action=action, result="Partial", docker=DockerList(affected=affected, ids=affectedList))

    if(invalidList):
        if(totalCount == 0): #totalCount can be 0 if and only all the data is invalid because totalCount represent all existing containers
            response.result = "Invalid"
        response.invalid = invalidList
    return response