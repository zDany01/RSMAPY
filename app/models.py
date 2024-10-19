from pydantic import BaseModel, PositiveInt, model_validator
from typing import Literal, Optional, Self

class DockerInput(BaseModel):
    containers: Optional[list[str]] = None
    containerNames: Optional[list[str]] = None

    @model_validator(mode="after")
    def checkEmpty(self: Self) -> Self:
        if (len(self.containers) if self.containers else 0) + (len(self.containerNames) if self.containerNames else 0) == 0:
            raise ValueError("The combined sent values does not indicate at least 1 container")
        return self

class BasicResponse(BaseModel):
    result: Literal["Ok", "Partial", "None", "Received"]

class DateInfo(BaseModel):
    date: str
    timestamp: int

class DockerList(BaseModel):
    affected: PositiveInt
    ids: list[str]

class DockerAction(BasicResponse):
    action: str
    docker: Optional[DockerList] = None