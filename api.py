from fastapi import FastAPI, responses
from routers import server
from pylib import pyUtils

if not pyUtils.isSudo():
    print("Make sure to execute this API with sudo priviledges")
    exit(1)

api: FastAPI = FastAPI()

api.include_router(server.server)

@api.get("/", response_class=responses.PlainTextResponse, status_code=418)
@api.get("/status", response_class=responses.PlainTextResponse)
def healthCheck():
    return "OK"