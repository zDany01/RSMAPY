from pydantic import BaseModel, PositiveInt, model_validator
from typing import Literal, Optional, Self

class DockerInput(BaseModel):
    range: Literal["All", "Active", "Custom"]
    containers: Optional[list[str]] = None
    containerNames: Optional[list[str]] = None

    @model_validator(mode="after")
    def checkEmpty(self: Self) -> Self:
        if self.range == "Custom" and (len(self.containers) if self.containers else 0) + (len(self.containerNames) if self.containerNames else 0) == 0:
            raise ValueError("The combined sent values does not indicate at least 1 container")
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
    invalid: Optional[list[str]] = None