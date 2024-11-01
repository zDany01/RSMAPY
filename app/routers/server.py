from math import trunc
from fastapi import APIRouter, status, Response, Depends, HTTPException
from threading import Timer
from os.path import exists, getmtime
from time import localtime, strftime
from pylib import ProcessOutput, executeCommand
from pylib.security import verifyJWT
import config
import models
from openapi_examples import RECIVED_EXAMPLE

server = APIRouter(prefix="/server", dependencies=[Depends(verifyJWT)], tags=["Server Management"])

@server.get("/shutdown", status_code=status.HTTP_202_ACCEPTED, response_model=models.BasicResponse, responses={202: {"content": RECIVED_EXAMPLE}})
def shutdown():
    Timer(5, executeCommand, ["poweroff"]).start()
    return { "result": "Received" }

@server.get("/reboot", status_code=status.HTTP_202_ACCEPTED, response_model=models.BasicResponse, responses={202: {"content": RECIVED_EXAMPLE}})
def reboot():
    Timer(5, executeCommand, ["reboot"]).start()
    return { "result": "Received" }

@server.get("/backup", response_model=models.BasicResponse, responses={500: {}})
def backup():
    procout: ProcessOutput = executeCommand(config.BACKUP_SCRIPT_PATH, config.BACKUP_SCRIPT_ARGS, "Unable to execute the backup script", 500) 
    return { "result": "Ok" if procout.good else "Fail"}

@server.get("/updatedb", response_model=models.BasicResponse, summary="Update the NGiNX GeoIP Block Database", responses={500: {}})
def updateIPDB():
    procout: ProcessOutput = executeCommand(config.NGINX_DB_UPDATE_PATH, errormsg="Unable to execute the nginx update script", httpErrorCode=500) 
    return { "result": "Ok" if procout.good else "Fail"}

@server.get("/lastbak", response_model=models.DateInfo, summary="Get the last backup date", responses={404: {"description": "Unable to get the last backup date"}})
def lastBackup():
    if not exists(config.BACKUP_FLAG_PATH):
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    timestamp: int = trunc(getmtime(config.BACKUP_FLAG_PATH))
    return {
        "date": strftime("%b %-d, %Y - %I:%M:%S %p", localtime(timestamp)),
        "timestamp": timestamp
    }
        