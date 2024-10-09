from fastapi import FastAPI, responses
from routers import server

api: FastAPI = FastAPI()

api.include_router(server.server)

@api.get("/", response_class=responses.PlainTextResponse)
@api.get("/status", response_class=responses.PlainTextResponse)
def healthCheck():
    return "OK"