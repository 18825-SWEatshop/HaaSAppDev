from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
from typing import List
import jwt, os
from ..project_manager import create_project, user_can_access, get_project, _projects
from ..user_manager import UserManager

SECRET = os.getenv("JWT_SECRET", "dev-secret")

router = APIRouter()

PROJECT_NOT_FOUND_MSG = "Project not found"

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

    try:
        doc = create_project(
            projectId=p.projectId,
            name=p.name,
            description=p.description,
            authorized_users=final_authorized,
            owner=user,
        )
    except ValueError as exc:
        raise HTTPException(400, str(exc))
    UserManager.add_project_to_user(user, doc["projectId"])
    return {"ok": True, "projectId": doc["projectId"]}

@router.post("/join")
def api_join_project(req: ProjectJoin, user: str = Depends(current_user)):
    project = get_project(req.projectId)
    if not project:
        raise HTTPException(404, PROJECT_NOT_FOUND_MSG)
    if not user_can_access(user, req.projectId):
        raise HTTPException(403, "You are not authorized for this project")

    UserManager.add_project_to_user(user, project["projectId"])
    return {
        "ok": True,
        "projectId": project["projectId"],
        "name": project["name"],
        "description": project.get("description", ""),
        "owner": project["owner"],
        "authorizedUsers": project.get("authorizedUsers", []),
        "hardwareAllocations": project.get("hardwareAllocations", []),
    }

@router.get("/my-projects")
def api_get_user_projects(user: str = Depends(current_user)):
    joined_ids = UserManager.get_joined_projects(user)
    if not joined_ids:
        return []
    return list(_projects().find({
        "projectId": {"$in": joined_ids}
    }, {"_id": 0}))

@router.post("/confirm-access")
def api_confirm_user_access(req: CheckUserAccess, user: str = Depends(current_user)):
    project = get_project(req.projectId)
    if not project:
        raise HTTPException(404, PROJECT_NOT_FOUND_MSG)

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
        raise HTTPException(404, PROJECT_NOT_FOUND_MSG)

    # Check if user has access to view this project
    if not user_can_access(user, req.projectId):
        raise HTTPException(403, "You are not authorized to view this project")

    return {
        "ok": True,
        "projectId": project["projectId"],
        "name": project["name"],
        "description": project.get("description", ""),
        "owner": project["owner"],
        "authorizedUsers": project.get("authorizedUsers", []),
        "hardwareAllocations": project.get("hardwareAllocations", [])  # Placeholder for future implementation
    }
