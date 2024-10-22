from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from math import trunc
import bcrypt
from jose import JWTError, jwt
from secrets import token_hex
import config

JWT_SECRET = token_hex(32) if config.AUTH_SECRET == "Random" else config.AUTH_SECRET
loginEndpoint = OAuth2PasswordBearer("login")

def hash(data: str) -> str:
    return bcrypt.hashpw(bytes(data, encoding="UTF-8") , bcrypt.gensalt())

def verifyHash(plain: str, hash: str) -> bool:
    return bcrypt.checkpw(bytes(plain, encoding="UTF-8"), bytes(config.AUTH_PASSWORD_HASH, encoding="UTF-8"))

def createJWT(data: dict, expireDelta: timedelta = timedelta(minutes=config.TOKEN_TIMEOUT)) -> str:
    tokenData = data.copy()
    tokenData.update({"expire": trunc((datetime.now() + expireDelta).timestamp())})
    return jwt.encode(tokenData, JWT_SECRET, "HS256")

def verifyJWT(token: str = Depends(loginEndpoint)) -> dict:
    try:
        data = jwt.decode(token, JWT_SECRET)
        if trunc(datetime.now().timestamp()) > int(data["expire"]):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Expired access token", {"WWW-Authenticate": "Bearer"})
        return data
    except JWTError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid access token", {"WWW-Authenticate": "Bearer"})