from math import trunc
from typing import Literal
from .process_manager import ProcessOutput, executeCommand

def getContainers(activeOnly: bool = False) -> list[str]:
    containerlistprc: ProcessOutput = executeCommand("docker", ["ps", "-a", "-q"] if not activeOnly else ["ps", "-q"], "Unable to get container list", 500)
    return containerlistprc.output.splitlines() if containerlistprc.good else None

def getContainersData(Containers: Literal["ALL", "ACTIVE"] = "ACTIVE", formatString: str = "") -> str:
    return executeCommand("docker", ["ps", "-a", "--format", formatString] if Containers == "ALL" else ["ps", "--format", formatString], "Unable to get containers data", 500).output

def getContainerData(CtID: str, formatString: str = None) -> str:
    return executeCommand("docker", ["ps", "-a", "--filter", "id=" + CtID, "--format", formatString] if formatString is not None else ["ps", "-a", "--filter", "id=" + CtID], "Unable to get container data for CtID: " + CtID).output.strip()

def getContainerDataList(CtIDs: list[str], formatString: str = None) -> list[str]:
    dataList: list[str] = []
    for CtID in CtIDs:
        dataList.append(getContainerData(CtID, formatString))
    return dataList

def startContainer(CtID: str, startOnly: bool = True, errormsg: str = "") -> int:
    """
    :param errormsg: this message will be displayed if there is an error when executing the start/restart command NOT if the container is already started
    :return 0: if started correctly
    :return 1: if already started
    :return 2: if restarted correctly
    :return -1: if an error occured during starting/restarting
    """
    if getContainerData(CtID, "{{.Status}}").startswith("Up"):
        if (startOnly):
            return 1
        return 2 if executeCommand("docker", ["restart", CtID], errormsg).good else -1
    return 0 if executeCommand("docker", ["start", CtID], errormsg).good else -1

def startContainers(CtIDs: list[str], startOnly: bool = True) -> list[int]:
    startResult: list[int] = []
    for CtID in CtIDs:
        startResult.append(startContainer(CtID, startOnly))
    return startResult

def stopContainer(CtID: str, errormsg: str = "") -> int:
    """
    :param errormsg: this message will be displayed if there is an error when executing the stop command NOT if the container is already stopped
    :return 0: if stopped correctly
    :return 1: if already stopped
    :return -1: if an error occured during stopping
    """
    if getContainerData(CtID, "{{.Status}}").startswith("Exited"):
        return 1
    return 0 if executeCommand("docker", ["stop", CtID], errormsg).good else -1

def stopContainers(CtIDs: list[str]) -> list[int]:
    stopResults: list[int] = []
    for CtID in CtIDs:
        stopResults.append(stopContainer(CtID))
    return stopResults