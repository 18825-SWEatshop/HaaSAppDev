from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import jwt, os
from ..user_manager import UserManager

SECRET = os.getenv("JWT_SECRET", "dev-secret")

# Create new router
router = APIRouter()

class Creds(BaseModel):
    username: str
    password: str

@router.post("/register")
def register(c: Creds):
    if UserManager.user_exists(c.username):
        raise HTTPException(401, "User already exists")
    UserManager.add_user(c.username, c.password)
    token = jwt.encode({"u": c.username}, SECRET, algorithm="HS256")
    return {"token": token}

@router.post("/login")
def login(c: Creds):
    if not UserManager.login(c.username, c.password):
        raise HTTPException(401, "Invalid credentials")
    token = jwt.encode({"u": c.username}, SECRET, algorithm="HS256")
    return {"token": token}