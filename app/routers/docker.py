from fastapi import APIRouter
from pylib import DockerManager
from pylib.utils import DockerResponse
import models

docker = APIRouter(prefix="/docker", tags=["Docker Management"])

@docker.get("/stop", response_model=models.DockerAction)
def stopDockers():
    CtIDs : list[str] = DockerManager.getContainers(True)
    returnArray: list[str] = []
    for i, value in enumerate(DockerManager.stopContainers(CtIDs)):
        if value == 0:
            returnArray.append(CtIDs[i])
    return DockerResponse("stop", returnArray, len(CtIDs))


@docker.get("/start", response_model=models.DockerAction)
def startDockers():
    CtIDs : list[str] = DockerManager.getContainers()
    returnArray: list[str] = []
    for i, value in enumerate(DockerManager.startContainers(CtIDs, True)):
        if value == 0:
            returnArray.append(CtIDs[i])
    return DockerResponse("start", returnArray, len(CtIDs))
    
@docker.get("/restart", response_model=models.DockerAction)
def restartDockers():
    CtIDs : list[str] = DockerManager.getContainers(True)
    returnArray: list[str] = []
    for i, value in enumerate(DockerManager.startContainers(CtIDs, False)):
        if value == 2:
            returnArray.append(CtIDs[i])
    return DockerResponse("restart", returnArray, len(CtIDs))