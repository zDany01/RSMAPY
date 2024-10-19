from fastapi import APIRouter
from pylib import DockerManager
from pylib.utils import DockerResponse
from models import DockerAction, DockerInput

docker = APIRouter(prefix="/docker", tags=["Docker Management"])

@docker.post("/stop", response_model=DockerAction)
def stopDockers(dockerInput: DockerInput):
    CtIDs: list[str]
    invalid: list[str] = None
    if dockerInput.range == "Custom":
        (CtIDs, invalid) = DockerManager.parseContainers(dockerInput.containers, dockerInput.containerNames)
    else:
        CtIDs = DockerManager.getContainers(dockerInput.range == "Active")

    successList: list[str] = []
    for i, value in enumerate(DockerManager.stopContainers(CtIDs)):
        if value == 0:
            successList.append(CtIDs[i])
    return DockerResponse("stop", successList, len(CtIDs), invalid)


@docker.post("/start", response_model=DockerAction)
def startDockers(dockerInput: DockerInput):
    CtIDs: list[str]
    invalid: list[str] = None
    if dockerInput.range == "Custom":
        (CtIDs, invalid) = DockerManager.parseContainers(dockerInput.containers, dockerInput.containerNames)
    else:
        CtIDs = DockerManager.getContainers(dockerInput.range == "Active")

    successList: list[str] = []
    for i, value in enumerate(DockerManager.startContainers(CtIDs, True)):
        if value == 0:
            successList.append(CtIDs[i])
    return DockerResponse("start", successList, len(CtIDs), invalid)
    
@docker.post("/restart", response_model=DockerAction)
def restartDockers(dockerInput: DockerInput):
    CtIDs: list[str]
    invalid: list[str] = None
    if dockerInput.range == "Custom":
        (CtIDs, invalid) = DockerManager.parseContainers(dockerInput.containers, dockerInput.containerNames)
    else:
        CtIDs = DockerManager.getContainers(dockerInput.range == "Active")

    successList: list[str] = []
    for i, value in enumerate(DockerManager.startContainers(CtIDs, False)):
        if value == 2:
            successList.append(CtIDs[i])
    return DockerResponse("restart", successList, len(CtIDs), invalid)