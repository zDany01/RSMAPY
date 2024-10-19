from fastapi import APIRouter
from pylib import DockerManager
from pylib.utils import DockerResponse, filterProtected
from models import DockerAction, DockerInput

dockers = APIRouter(prefix="/dockers", tags=["Docker Management"])

@dockers.post("/stop", response_model=DockerAction)
def stopDockers(dockerInput: DockerInput):
    CtIDs: list[str]
    invalid: list[str] = None
    if dockerInput.range == "Custom":
        (CtIDs, invalid) = DockerManager.parseContainers(dockerInput.containers, dockerInput.containerNames)
    else:
        CtIDs = DockerManager.getContainers(dockerInput.range == "Active")

    oLenght: int = len(CtIDs)
    CtIDs = filterProtected(CtIDs)
    successList: list[str] = []
    for i, value in enumerate(DockerManager.stopContainers(CtIDs)):
        if value == 0:
            successList.append(CtIDs[i])
    return DockerResponse("stop", successList, len(CtIDs), oLenght, invalid)


@dockers.post("/start", response_model=DockerAction)
def startDockers(dockerInput: DockerInput):
    CtIDs: list[str]
    invalid: list[str] = None
    if dockerInput.range == "Custom":
        (CtIDs, invalid) = DockerManager.parseContainers(dockerInput.containers, dockerInput.containerNames)
    else:
        CtIDs = DockerManager.getContainers(dockerInput.range == "Active")

    lenght: int = len(CtIDs)
    successList: list[str] = []
    for i, value in enumerate(DockerManager.startContainers(CtIDs, True)):
        if value == 0:
            successList.append(CtIDs[i])
    return DockerResponse("start", successList, lenght, lenght, invalid)
    
@dockers.post("/restart", response_model=DockerAction)
def restartDockers(dockerInput: DockerInput):
    CtIDs: list[str]
    invalid: list[str] = None
    if dockerInput.range == "Custom":
        (CtIDs, invalid) = DockerManager.parseContainers(dockerInput.containers, dockerInput.containerNames)
    else:
        CtIDs = DockerManager.getContainers(dockerInput.range == "Active")

    oLenght: int = len(CtIDs)
    CtIDs = filterProtected(CtIDs)
    successList: list[str] = []
    for i, value in enumerate(DockerManager.startContainers(CtIDs, False)):
        if value == 2:
            successList.append(CtIDs[i])
    return DockerResponse("restart", successList, len(CtIDs), oLenght, invalid)