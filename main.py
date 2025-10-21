from fastapi import FastAPI, HTTPException, Depends, Request
from pydantic import BaseModel
from typing import List, Optional
import os, jwt
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

from .user_manager import UserManager
from .project_manager import create_project, user_can_access, get_project  # <-- if you added this file


load_dotenv()
SECRET = os.getenv("JWT_SECRET", "dev-secret")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:3000"] if you want to restrict it
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def current_user(request: Request) -> str:
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        raise HTTPException(401, "Missing token")
    token = auth.split(" ", 1)[1]
    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        return payload["u"]
    except Exception:
        raise HTTPException(401, "Invalid token")

class ProjectCreate(BaseModel):
    projectId: str
    name: str
    description: str
    authorizedUsers: List[str] = []

class ProjectLogin(BaseModel):
    projectId: str

@app.post("/projects/create")
def api_create_project(p: ProjectCreate, user: str = Depends(current_user)):
    if get_project(p.projectId):
        raise HTTPException(400, "Project ID already exists")
    norm_users = [u.strip() for u in p.authorizedUsers if u.strip()]
    creator = user
    auth_set = set(norm_users)
    auth_set.add(creator)
    final_authorized = sorted(auth_set)

    doc = create_project(
        projectId=p.projectId,
        name=p.name,
        description=p.description,
        authorized_users=final_authorized,
        owner=user,
    )
    return {"ok": True, "projectId": doc["projectId"]}

@app.post("/projects/login")
def api_login_project(req: ProjectLogin, user: str = Depends(current_user)):
    if not get_project(req.projectId):
        raise HTTPException(404, "Project not found")
    if not user_can_access(user, req.projectId):
        raise HTTPException(403, "You are not authorized for this project")
    # success — return minimal project info (expand later if you want)
    p = get_project(req.projectId)
    return {
        "ok": True,
        "projectId": p["projectId"],
        "name": p["name"],
        "owner": p["owner"],
        "authorizedUsers": p.get("authorizedUsers", []),
        "description": p.get("description", ""),
    }

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
