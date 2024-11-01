from fastapi import APIRouter, HTTPException, status
from pylib.security import verifyHash, createJWT
from models import LoginInfo, LoginResponse
from config import AUTH_USERNAME, AUTH_PASSWORD_HASH

auth = APIRouter()

@auth.post("/login", response_model=LoginResponse, summary="Login with credentials", tags=["API"], responses={404: {"description": "Invalid Credentials"}})
def login(userInfo: LoginInfo):
    if userInfo.username == AUTH_USERNAME and verifyHash(userInfo.password, AUTH_PASSWORD_HASH):
        return {"token": createJWT({})}
    raise HTTPException(status.HTTP_404_NOT_FOUND, "Invalid Credentials")