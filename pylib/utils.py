import os

def isSudo() -> bool:
    try:
        return os.getuid() == 0
    except AttributeError:
        print("This API can only be executed on Linux")
        exit(182)