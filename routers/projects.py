from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
from typing import List
import jwt, os
from ..project_manager import create_project, user_can_access, get_project, _projects, add_user_to_project

SECRET = os.getenv("JWT_SECRET", "dev-secret")

router = APIRouter()

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
    projectID: str
    name: str
    description: str
    authorizedUsers: List[str] = []

class ProjectJoin(BaseModel):
    projectID : str

class AddUserToProject(BaseModel):
    projectID: str
    username: str

@router.post("/create")
def api_create_project(p: ProjectCreate, user: str = Depends(current_user)):
    if get_project(p.projectID):
        raise HTTPException(400, "Project ID already exists")
    norm_users = [u.strip() for u in p.authorizedUsers if u.strip()]
    creator = user
    auth_set = set(norm_users)
    auth_set.add(creator)
    final_authorized = sorted(auth_set)

    doc = create_project(
        projectId=p.projectID,
        name=p.name,
        description=p.description,
        authorized_users=final_authorized,
        owner=user,
    )
    return {"ok": True, "projectId": doc["projectId"]}

@router.post("/join")
def api_join_project(req: ProjectJoin, user: str = Depends(current_user)):
    if not get_project(req.projectID):
        raise HTTPException(404, "Project not found")
    if not user_can_access(user, req.projectID):
        raise HTTPException(403, "You are not authorized for this project")
    # success — return minimal project info (expand later if you want)
    p = get_project(req.projectID)
    return {
        "ok": True,
        "projectId": p["projectId"],
        "name": p["name"],
        "owner": p["owner"],
        "authorizedUsers": p.get("authorizedUsers", []),
        "description": p.get("description", ""),
    }

@router.get("/my-projects")
def api_get_user_projects(user: str = Depends(current_user)):
    return list(_projects().find({
        "$or": [
            {"owner": user},
            {"authorizedUsers": user}
        ]
    }, {"_id": 0}))  # Exclude the _id field