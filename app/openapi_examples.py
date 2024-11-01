RECIVED_EXAMPLE = {
    "application/json": {
        "example": {
            "result": "Received"
        }
    }
}

RESTART_EXAMPLE = {
    "application/json": {
        "example": {
            "result": "Ok",
            "power": "Started"
        }
    }
}

PORT_EXAMPLE = {
    "application/json": {
        "example": {
            "<PORT>/<PROTOCOL>": [
                {
                    "HostIp": "<IP Socket>",
                    "HostPort": "<PORT>"
                }
            ]
        }
    }
}

DOCKER_INPUT_EXAMPLES = {
    "All": {
        "summary": "All Containers",
        "value": {
            "range": "All"
        }
    },
    "Active": {
        "summary": "Active Containers",
        "value": {
            "range": "Active"
        }
    },
    "Custom": {
        "value": {
            "range": "Custom",
            "containers": ["CtID1, CtID2, ..."],
            "containerNames": ["CtName1, ..."]
        }
    },
    "Custom1": {
        "value": {
            "range": "Custom",
            "containers": ["CtID1, CtID2, ..."]
        }
    },
    "Custom2": {
        "value": {
            "range": "Custom",
            "containerNames": ["CtName1, ..."]
        }
    }
}

def generateDockerActionExample(action: str) -> dict:
    return \
{
    "application/json": {
        "examples": {
            "Ok": {
                "summary": "All executed correctly",
                "value": {
                    "result": "Ok",
                    "action": action,
                    "protectionSkip": False
                }
            },
            "Valid": {
                "summary": "All existing executed correctly",
                "value": {
                    "result": "Valid",
                    "action": action,
                    "protectionSkip": False,
                    "invalid": [
                        "string"
                    ]
                }
            },
            "Partial": {
                "summary": "Partial execution",
                "value": {
                    "result": "Partial",
                    "action": action,
                    "docker": {
                        "affected": 2,
                        "ids": [
                        "CtID_1",
                        "CtID_2"
                        ]
                    },
                    "protectionSkip": False
                }
            },
            "PartialInv": {
                "summary": "Partial execution and invalid data",
                "value": {
                    "result": "Partial",
                    "action": action,
                    "docker": {
                        "affected": 2,
                        "ids": [
                        "CtID_1",
                        "CtID_2"
                        ]
                    },
                    "protectionSkip": False,
                    "invalid": [
                        "string"
                    ]
                }
            },
            "None": {
                "summary": "None of the element",
                "value": {
                    "result": "None",
                    "action": action,
                    "protectionSkip": False
                }
            },
            "Invalid": {
                "summary": "None of the element exists",
                "value": {
                    "result": "Invalid",
                    "action": action,
                    "protectionSkip": False,
                    "invalid": [
                        "string"
                    ]
                }
            }
        }
    }
}

def generatePowerStatusExample(powerSuccess: str, powerFail: str) -> dict:
    return \
{
    "application/json": {
        "examples": {
            "Ok": {
                "summary": "Success",
                "value": {
                    "result": "Ok",
                    "power": powerSuccess
                }
            },
            "Bad": {
                "summary": "Failure",
                "value": {
                    "result": "None",
                    "power": powerFail
                }
            }
        }
    }
}