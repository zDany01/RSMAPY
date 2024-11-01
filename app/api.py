from fastapi import FastAPI, responses
from fastapi.middleware.cors import CORSMiddleware
from routers import ServerRouter, DockersRouter, DockerRouter, AuthRouter
from pylib import pyUtils

pyUtils.preBootCheck()

api: FastAPI = FastAPI(title="RSMAPY", description="A python API to remotely manage a server", version="0.1", license_info={"name": "MIT License", "identifier": "MIT", "url": "https://github.com/zDany01/RSMAPY/blob/main/LICENSE"})

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api.include_router(AuthRouter)
api.include_router(ServerRouter)
api.include_router(DockersRouter)
api.include_router(DockerRouter)

@api.get("/", response_class=responses.PlainTextResponse, status_code=418, tags=["API"], summary=" ")
@api.get("/status", response_class=responses.PlainTextResponse, tags=["API"], summary="Get server status")
def healthCheck():
    return "OK"