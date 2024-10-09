from fastapi import APIRouter

server = APIRouter(tags=["Server Management"])

@server.get("/shutdown")
def shutdown():
    print("Server shutted down")
    return {"Operation": "Success"}