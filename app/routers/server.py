from math import trunc
from fastapi import APIRouter, status, Response, Depends
from threading import Timer
from os.path import exists, getmtime
from time import localtime, strftime
from pylib import ProcessOutput, executeCommand
from pylib.security import verifyJWT
import config
import models

server = APIRouter(prefix="/server", tags=["Server Management"])

@server.get("/shutdown", status_code=status.HTTP_202_ACCEPTED, response_model=models.BasicResponse)
def shutdown(_ = Depends(verifyJWT)):
    Timer(5, executeCommand, ["poweroff"]).start()
    return { "result": "Received" }

@server.get("/reboot", status_code=status.HTTP_202_ACCEPTED, response_model=models.BasicResponse)
def reboot(_ = Depends(verifyJWT)):
    Timer(5, executeCommand, ["reboot"]).start()
    return { "result": "Received" }

@server.get("/backup", response_model=models.BasicResponse)
def backup(_ = Depends(verifyJWT)):
    procout: ProcessOutput = executeCommand(config.BACKUP_SCRIPT_PATH, config.BACKUP_SCRIPT_ARGS, "Unable to execute the backup script", 500) 
    return { "result": "Ok" if procout.good else "Fail"}

@server.get("/updatedb", response_model=models.BasicResponse)
def updateIPDB(_ = Depends(verifyJWT)):
    procout: ProcessOutput = executeCommand(config.NGINX_DB_UPDATE_PATH, errormsg="Unable to execute the nginx update script", httpErrorCode=500) 
    return { "result": "Ok" if procout.good else "Fail"}

@server.get("/lastbak", response_description="Return 204 if the last backup can't be found otherwise it returns the date", response_model=models.DateInfo)
def lastBackup(response: Response, _ = Depends(verifyJWT)):
    if not exists(config.BACKUP_FLAG_PATH):
        response.status_code = 204
        return
    timestamp: int = trunc(getmtime(config.BACKUP_FLAG_PATH))
    return {
        "date": strftime("%b %-d, %Y - %I:%M:%S %p", localtime(timestamp)),
        "timestamp": timestamp
        }
        