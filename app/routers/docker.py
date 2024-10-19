from fastapi import APIRouter, HTTPException, status
from fastapi.responses import PlainTextResponse
from pylib import DockerManager, executeCommand
from models import DockerPowerStatus
from json import loads

docker = APIRouter(prefix="/docker/{CtID}", tags=["Single Container"])

@docker.get("/")
def dockerInfo(CtID: str):
    if not DockerManager.getContainerData(CtID, "{{.ID}}"):
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return loads(executeCommand("docker", ["inspect", CtID], "Unable to access the container with ID " + CtID, 500).output)[0]

@docker.get("/stop", response_model=DockerPowerStatus)
def stopContainer(CtID: str):
    if not DockerManager.getContainerData(CtID, "{{.ID}}"):
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return DockerPowerStatus(result="None", power="Down") if DockerManager.stopContainer(CtID, "Unable to stop the container with ID " + CtID) else DockerPowerStatus(result="Ok", power="Stopped")

@docker.get("/start", response_model=DockerPowerStatus)
def startContainer(CtID: str):
    if not DockerManager.getContainerData(CtID, "{{.ID}}"):
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return DockerPowerStatus(result="None", power="Up") if DockerManager.startContainer(CtID, errormsg="Unable to stop the container with ID " + CtID) else DockerPowerStatus(result="Ok", power="Started")


@docker.get("/restart", response_model=DockerPowerStatus)
def restartContainer(CtID: str):
    if not DockerManager.getContainerData(CtID, "{{.ID}}"):
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    DockerManager.startContainer(CtID, False, "Unable to stop the container with ID " + CtID)
    #it is useless to check because either 0 or 2 have the same output message
    #1 isn't one of the results since if the container is started the function restarts it
    #-1 is automatically managed by the executecommmand function since it has an errormsg
    return DockerPowerStatus(result="Ok", power="Started")

@docker.get("/ports")
def getContainerPorts(CtID: str):
    if not DockerManager.getContainerData(CtID, "{{.ID}}"):
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    json: dict = loads(executeCommand("docker", ["inspect", CtID, "--format", "{{json .NetworkSettings.Ports}}"], "Unable to access the published port of CtID " + CtID, 500).output)
    if not len(json):
        raise HTTPException(status.HTTP_204_NO_CONTENT)
    return json

@docker.get("/logs", response_class=PlainTextResponse)
def getContainerLogs(CtID: str):
    if not DockerManager.getContainerData(CtID, "{{.ID}}"):
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    logs: str = executeCommand("docker", ["logs", CtID], "Unable to get logs for CtID " + CtID, 500).output
    if not len(logs.strip()):
        raise HTTPException(status.HTTP_204_NO_CONTENT)
    return logs