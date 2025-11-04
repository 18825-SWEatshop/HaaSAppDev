from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
from typing import List
import jwt, os
from ..project_manager import create_project, user_can_access, get_project, _projects

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
    projectId: str
    name: str
    description: str
    authorizedUsers: List[str] = []

class ProjectJoin(BaseModel):
    projectId : str

class AddUserToProject(BaseModel):
    projectId: str
    username: str

class CheckUserAccess(BaseModel):
    projectId: str

class GetProjectDetails(BaseModel):
    projectId: str

@router.post("/create")
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

@router.post("/join")
def api_join_project(req: ProjectJoin, user: str = Depends(current_user)):
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

@router.get("/my-projects")
def api_get_user_projects(user: str = Depends(current_user)):
    return list(_projects().find({
        "$or": [
            {"owner": user},
            {"authorizedUsers": user}
        ]
    }, {"_id": 0}))  # Exclude the _id field

@router.post("/confirm-access")
def api_confirm_user_access(req: CheckUserAccess, user: str = Depends(current_user)):
    project = get_project(req.projectId)
    if not project:
        raise HTTPException(404, "Project not found")

    has_access = user_can_access(user, req.projectId)

    return {
        "ok": True,
        "projectId": req.projectId,
        "hasAccess": has_access,
        "isOwner": project["owner"] == user,
        "isAuthorizedUser": user in project.get("authorizedUsers", [])
    }

@router.post("/details")
def api_get_project_details(req: GetProjectDetails, user: str = Depends(current_user)):
    project = get_project(req.projectId)
    if not project:
        raise HTTPException(404, "Project not found")

    # Check if user has access to view this project
    if not user_can_access(user, req.projectId):
        raise HTTPException(403, "You are not authorized to view this project")

    # For now, hardware allocations and joinedUsers are not implemented yet
    return {
        "ok": True,
        "projectId": project["projectId"],
        "name": project["name"],
        "description": project.get("description", ""),
        "owner": project["owner"],
        "authorizedUsers": project.get("authorizedUsers", []),
        "createdAt": project.get("createdAt"),
        "joinedUsers": project.get("joinedUsers", []),  # Placeholder for future implementation
        "hardwareAllocations": project.get("hardwareAllocations", [])  # Placeholder for future implementation
    }
