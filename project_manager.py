from datetime import datetime
from typing import Optional, List
from .database import db

def _projects():
    if db is None:
        raise RuntimeError("Database not connected.")
    col = db["projects"]
    col.create_index("projectId", unique=True)
    return col

def create_project(*, projectId: str, name: str, description: str, authorized_users: List[str], owner: str):
    doc = {
        "projectId": projectId.strip(),
        "name": name.strip(),
        "description": description.strip(),
        "authorizedUsers": [u.strip() for u in authorized_users if u.strip()],
        "owner": owner,
        "createdAt": datetime.utcnow(),
    }
    _projects().insert_one(doc)
    return doc

def get_project(projectId: str) -> Optional[dict]:
    return _projects().find_one({"projectId": projectId})

def user_can_access(username: str, projectId: str) -> bool:
    p = get_project(projectId)
    if not p:
        return False
    return username == p["owner"] or username in p.get("authorizedUsers", [])

def add_user_to_project(projectId: str, username: str, requester: str) -> bool:
    """Add a user to a project's authorized users list. Only project owner can do this."""
    project = get_project(projectId)
    if not project:
        return False
    
    # Only the project owner can add users
    if project["owner"] != requester:
        return False
    
    # Don't add if user is already authorized or is the owner
    if username == project["owner"] or username in project.get("authorizedUsers", []):
        return False
    
    # Add user to authorized users list
    _projects().update_one(
        {"projectId": projectId},
        {"$push": {"authorizedUsers": username}}
    )
    return True
