from fastapi import APIRouter, Body, Depends
from pylib import DockerManager
from pylib.utils import DockerResponse, filterProtected
from pylib.security import verifyJWT
from models import DockerAction, DockerInput
from typing import Annotated
from openapi_examples import generateDockerActionExample, DOCKER_INPUT_EXAMPLES

dockers = APIRouter(prefix="/dockers", tags=["Docker Management"])

@dockers.post("/stop", response_model=DockerAction, summary="Stop a range of docker containers", responses={200: {"content": generateDockerActionExample("stop")}})
def stopDockers(dockerInput: Annotated[DockerInput, Body(openapi_examples=DOCKER_INPUT_EXAMPLES)],  _ = Depends(verifyJWT)):
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


@dockers.post("/start", response_model=DockerAction, summary="Start a range of docker containers", responses={200: {"content": generateDockerActionExample("start")}})
def startDockers(dockerInput: Annotated[DockerInput, Body(openapi_examples=DOCKER_INPUT_EXAMPLES)], _ = Depends(verifyJWT)):
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
    
@dockers.post("/restart", response_model=DockerAction, summary="Restart a range of docker containers", responses={200: {"content": generateDockerActionExample("restart")}})
def restartDockers(dockerInput: Annotated[DockerInput, Body(openapi_examples=DOCKER_INPUT_EXAMPLES)], _ = Depends(verifyJWT)):
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