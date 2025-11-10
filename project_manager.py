from datetime import datetime, timezone
from typing import Optional, List
from pymongo import ReturnDocument
from pymongo.errors import DuplicateKeyError

from .database import db

PROJECT_NOT_FOUND_MSG = "Project not found"
INVALID_SET_MSG = "Invalid set number"

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
        "hardwareAllocations": [0, 0],
        "createdAt": datetime.now(timezone.utc),
    }
    try:
        _projects().insert_one(doc)
    except DuplicateKeyError as exc:
        raise ValueError("Project ID already exists") from exc
    return doc

def get_project(projectId: str) -> Optional[dict]:
    return _projects().find_one({"projectId": projectId})

def user_can_access(username: str, projectId: str) -> bool:
    p = get_project(projectId)
    if not p:
        return False
    return username == p["owner"] or username in p.get("authorizedUsers", [])

def get_hardware_allocation(projectId: str, set_number: int) -> int:
    project = get_project(projectId)
    if not project:
        raise ValueError(PROJECT_NOT_FOUND_MSG)
    allocations = project.get("hardwareAllocations", [])
    if set_number < 1 or set_number > len(allocations):
        raise ValueError(INVALID_SET_MSG)
    return allocations[set_number - 1]

def increase_hardware_allocation(projectId: str, set_number: int, quantity: int) -> dict:
    if set_number < 1:
        raise ValueError(INVALID_SET_MSG)
    index = set_number - 1
    update_result = _projects().find_one_and_update(
        {"projectId": projectId},
        {"$inc": {f"hardwareAllocations.{index}": quantity}},
        return_document=ReturnDocument.AFTER,
    )
    if not update_result:
        raise ValueError(PROJECT_NOT_FOUND_MSG)
    return update_result

def decrease_hardware_allocation(projectId: str, set_number: int, quantity: int) -> dict:
    if set_number < 1:
        raise ValueError(INVALID_SET_MSG)
    index = set_number - 1
    project = get_project(projectId)
    if not project:
        raise ValueError(PROJECT_NOT_FOUND_MSG)
    current_allocation = project.get("hardwareAllocations", [0, 0])[index]
    if current_allocation < quantity:
        raise ValueError("Insufficient hardware allocation to decrease")
    update_result = _projects().find_one_and_update(
        {"projectId": projectId},
        {"$inc": {f"hardwareAllocations.{index}": -quantity}},
        return_document=ReturnDocument.AFTER,
    )
    return update_result
