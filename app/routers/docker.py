from fastapi import APIRouter
from pylib import DockerManager

docker = APIRouter(prefix="/docker", tags=["Docker Management"])

@docker.get("/stop")
def stopDockers():
    CtIDs : list[str] = DockerManager.getContainers(True)
    returnArray: list[str] = []
    for i, value in enumerate(DockerManager.stopContainers(CtIDs)):
        if value == 0:
            returnArray.append(CtIDs[i])
    
    stoppedCount: int = len(returnArray)
    if(stoppedCount == 0):
        return {"result": "None"}
    elif (stoppedCount == len(CtIDs)):
        return {"result": "Ok"}
    else:
        return {
                "result": "Partial",
                "docker": {
                    "stopped": stoppedCount,
                    "ctIDs": returnArray
                }
            }


@docker.get("/start")
def startDockers():
    CtIDs : list[str] = DockerManager.getContainers()
    returnArray: list[str] = []
    for i, value in enumerate(DockerManager.startContainers(CtIDs, True)):
        if value == 0:
            returnArray.append(CtIDs[i])
    
    startedCount: int = len(returnArray)
    if(startedCount == 0):
        return {"result": "None"}
    elif (startedCount == len(CtIDs)):
        return {"result": "Ok"}
    else:
        return {
                "result": "Partial",
                "docker": {
                    "started": startedCount,
                    "ctIDs": returnArray
                }
            }
    
@docker.get("/restart")
def restartDockers():
    CtIDs : list[str] = DockerManager.getContainers(True)
    returnArray: list[str] = []
    for i, value in enumerate(DockerManager.startContainers(CtIDs, False)):
        if value == 2:
            returnArray.append(CtIDs[i])
    
    restartedCount: int = len(returnArray)
    if(restartedCount == 0):
        return {"result": "None"}
    elif (restartedCount == len(CtIDs)):
        return {"result": "Ok"}
    else:
        return {
                "result": "Partial",
                "docker": {
                    "restarted": restartedCount,
                    "ctIDs": returnArray
                }
            }