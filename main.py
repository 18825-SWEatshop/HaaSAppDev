from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os, jwt
from dotenv import load_dotenv
from .user_manager import UserManager

load_dotenv()
SECRET = os.getenv("JWT_SECRET", "dev-secret")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Creds(BaseModel):
    username: str
    password: str

@app.post("/register")
def register(c: Creds):
    if UserManager.user_exists(c.username):
        raise HTTPException(401, "User already exists")
    UserManager.add_user(c.username, c.password)
    token = jwt.encode({"u": c.username}, SECRET, algorithm="HS256")
    return {"token": token}

@app.post("/login")
def login(c: Creds):
    if not UserManager.login(c.username, c.password):
        raise HTTPException(401, "Invalid credentials")
    token = jwt.encode({"u": c.username}, SECRET, algorithm="HS256")
    return {"token": token}
