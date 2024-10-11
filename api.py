from fastapi import FastAPI, responses
from routers import server
from pylib import pyUtils

pyUtils.preBootCheck()

api: FastAPI = FastAPI()

api.include_router(server.server)

@api.get("/", response_class=responses.PlainTextResponse, status_code=418)
@api.get("/status", response_class=responses.PlainTextResponse)
def healthCheck():
    return "OK"