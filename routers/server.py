from fastapi import APIRouter, status
from threading import Timer
from pylib import ProcessOutput, executeCommand
import config

server = APIRouter(prefix="/server", tags=["Server Management"])

@server.get("/shutdown", status_code=status.HTTP_202_ACCEPTED)
def shutdown():
    Timer(5, executeCommand, ["poweroff"]).start()
    return { "result": "Received" }

@server.get("/reboot", status_code=status.HTTP_202_ACCEPTED)
def reboot():
    Timer(5, executeCommand, ["reboot"]).start()
    return { "result": "Received" }

@server.get("/backup")
def backup():
    procout: ProcessOutput = executeCommand(config.BACKUP_SCRIPT_PATH, config.BACKUP_SCRIPT_ARGS, "Unable to execute the backup script", 500) 
    return { "result": "Ok" if procout.good else "Fail"}

@server.get("/updatedb")
def updateIPDB():
    procout: ProcessOutput = executeCommand(config.NGINX_DB_UPDATE_PATH, errormsg="Unable to execute the nginx update script", httpErrorCode=500) 
    return { "result": "Ok" if procout.good else "Fail"}