from pydantic import BaseModel, PositiveInt, model_validator
from typing import Literal, Optional, Self

class DockerInput(BaseModel):
    range: Literal["All", "Active", "Custom"]
    containers: Optional[list[str]] = None
    containerNames: Optional[list[str]] = None

    @model_validator(mode="after")
    def checkEmpty(self: Self) -> Self:
        if(self.range == "Custom"):  
            fcontainers: list[str] = []
            fcontainerNames: list[str] = []
            
            if(self.containers):
                for ct in self.containers:
                    if(ct.strip()): #checks if a string is not void or whitespace
                        fcontainers.append(ct)
            if(self.containerNames):
                for ctn in self.containerNames:
                    if(ctn.strip()):
                        fcontainerNames.append(ctn)

            if len(fcontainers) + len(fcontainerNames) == 0:
                raise ValueError("The combined sent values does not indicate at least 1 container")
            
            self.containers = fcontainers
            self.containerNames = fcontainerNames
        return self

class BasicResponse(BaseModel):
    result: Literal["Ok", "Valid", "Partial", "None", "Invalid", "Received"]

class DateInfo(BaseModel):
    date: str
    timestamp: int

class DockerList(BaseModel):
    affected: PositiveInt
    ids: list[str]

class DockerAction(BasicResponse):
    action: str
    docker: Optional[DockerList] = None
    protectionSkip: bool
    invalid: Optional[list[str]] = None

class DockerPowerStatus(BasicResponse):
    power: Literal["Stopped", "Started", "Up", "Down"]

class LoginInfo(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    token: str