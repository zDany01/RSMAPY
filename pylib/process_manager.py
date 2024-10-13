from threading import Lock
from subprocess import Popen, PIPE
from fastapi import HTTPException
import logging

lg = logging.getLogger("uvicorn.RSMAPY")

threadLock = Lock()

class ProcessOutput:
    def __init__(self, exitcode: int, output: str):
        self.ecode = exitcode
        self.output = output
        self.good = exitcode == 0

def executeCommand(path: str, args: list[str | int | bool,] = [], errormsg: str = "", httpErrorCode: int = 422) -> ProcessOutput:
    threadLock.acquire()
    command: list[str] = [path]
    command.extend(args)
    lg.info(f"Executing {path} with args: " + "".join(map(lambda c: c + ' ' ,map(str, args))))

    try:
        global exitcode
        global output
        global err
        process = Popen(command, stdout=PIPE, stderr=PIPE)
        (output, err) = process.communicate()
        exitcode = process.wait()
    except ValueError as err2:
        exitcode = -1
        lg.error("[PYTHON ERROR] - " + err2.decode("utf-8"))
        raise HTTPException(500)
    finally:
        threadLock.release()

    if exitcode != 0:
        logmsg: str = "Executing command: "
        for part in command:
            logmsg += f'|{part}|'
        lg.error(f"{logmsg}\n\t  Generated this error: {err.decode('utf-8')}")
        if(errormsg):
            raise HTTPException(httpErrorCode, errormsg)
    else:
        lg.debug("Execution finished")
    return ProcessOutput(exitcode, output.decode("utf-8"))