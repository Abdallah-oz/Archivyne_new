import os
from fastapi import APIRouter, HTTPException

from .schemas import LoginRequest, Token
from .services import verify_password, create_access_token


router=APIRouter(prefix="/auth", tags=["auth"])
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD_HASH = os.getenv("ADMIN_PASSWORD_HASH")

@router.post("/login",response_model=Token)
async def login(credentials:LoginRequest):
     if credentials.username != ADMIN_USERNAME:
        raise HTTPException(status_code=401, detail="Invalid credentials")

     if not verify_password(credentials.password, ADMIN_PASSWORD_HASH):
        raise HTTPException(status_code=401, detail="Invalid credentials")
     access_token = create_access_token(data={"sub": credentials.username})
     return {"access_token": access_token, "token_type": "bearer"}


from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

