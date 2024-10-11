from threading import Lock
from subprocess import Popen, PIPE
from fastapi import HTTPException

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
    print(f"Executing {path} with args: " + "".join(map(lambda c: c + ' ' ,map(str, args))))

    try:
        global exitcode
        global output
        process = Popen(command, stdout=PIPE)
        (output, err) = process.communicate()
        exitcode = process.wait()
    except ValueError as err2:
        exitcode = -1
        print("[PYTHON ERROR] - " + err2.decode("utf-8"))
        raise HTTPException(500)
    finally:
        threadLock.release()

    if exitcode != 0:
        print("Executing command: ", end='')
        for part in command:
            print('|' + part + '|', end=' ')
        print()
        print("Generated this error:" + output.decode("utf-8"))
        if(errormsg):
            raise HTTPException(httpErrorCode, errormsg)
    return ProcessOutput(exitcode, output.decode("utf-8"))