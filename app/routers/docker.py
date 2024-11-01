from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import PlainTextResponse
from pylib import DockerManager, executeCommand
from pylib.security import verifyJWT
from models import DockerPowerStatus
from json import loads
from openapi_examples import generatePowerStatusExample, RESTART_EXAMPLE, PORT_EXAMPLE

docker = APIRouter(prefix="/docker/{CtID}", tags=["Single Container"])

@docker.get("/", responses={404: {"description": "Unable to find the specified container"}, 500: {}}, summary="Get info about a container")
def dockerInfo(CtID: str, _ = Depends(verifyJWT)):
    if not DockerManager.getContainerData(CtID, "{{.ID}}"):
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return loads(executeCommand("docker", ["inspect", CtID], "Unable to access the container with ID " + CtID, 500).output)[0]

@docker.get("/stop", response_model=DockerPowerStatus, responses={200: {"content": generatePowerStatusExample("Stopped", "Down")}, 404: {"description": "Unable to find the specified container"}}, summary="Stop a container")
def stopContainer(CtID: str, _ = Depends(verifyJWT)):
    if not DockerManager.getContainerData(CtID, "{{.ID}}"):
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return DockerPowerStatus(result="None", power="Down") if DockerManager.stopContainer(CtID, "Unable to stop the container with ID " + CtID) else DockerPowerStatus(result="Ok", power="Stopped")

@docker.get("/start", response_model=DockerPowerStatus, responses={200: {"content": generatePowerStatusExample("Started", "Up")}, 404: {"description": "Unable to find the specified container"}}, summary="Start a container")
def startContainer(CtID: str, _ = Depends(verifyJWT)):
    if not DockerManager.getContainerData(CtID, "{{.ID}}"):
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return DockerPowerStatus(result="None", power="Up") if DockerManager.startContainer(CtID, errormsg="Unable to stop the container with ID " + CtID) else DockerPowerStatus(result="Ok", power="Started")


@docker.get("/restart", response_model=DockerPowerStatus, responses={200: {"content": RESTART_EXAMPLE}, 404: {"description": "Unable to find the specified container"}}, summary="Restart a container")
def restartContainer(CtID: str, _ = Depends(verifyJWT)):
    if not DockerManager.getContainerData(CtID, "{{.ID}}"):
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    DockerManager.startContainer(CtID, False, "Unable to stop the container with ID " + CtID)
    #it is useless to check because either 0 or 2 have the same output message
    #1 isn't one of the results since if the container is started the function restarts it
    #-1 is automatically managed by the executecommmand function since it has an errormsg
    return DockerPowerStatus(result="Ok", power="Started")

@docker.get("/ports", responses={200: {"content": PORT_EXAMPLE}, 204: {"description": "The container has no published ports"}, 404: {"description": "Unable to find the specified container"}}, summary="Get the published port of a container")
def getContainerPorts(CtID: str, _ = Depends(verifyJWT)):
    if not DockerManager.getContainerData(CtID, "{{.ID}}"):
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    json: dict = loads(executeCommand("docker", ["inspect", CtID, "--format", "{{json .NetworkSettings.Ports}}"], "Unable to access the published port of CtID " + CtID, 500).output)
    if not len(json):
        raise HTTPException(status.HTTP_204_NO_CONTENT)
    return json

@docker.get("/logs", response_class=PlainTextResponse, responses={204: {"description": "The container has no logs"}, 404: {"description": "Unable to find the specified container"}}, summary="Get the execution logs of a container")
def getContainerLogs(CtID: str, _ = Depends(verifyJWT)):
    if not DockerManager.getContainerData(CtID, "{{.ID}}"):
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    logs: str = executeCommand("docker", ["logs", CtID], "Unable to get logs for CtID " + CtID, 500).output
    if not len(logs.strip()):
        raise HTTPException(status.HTTP_204_NO_CONTENT)
    return logs