from typing import Optional, List
from passlib.hash import pbkdf2_sha256
from .database import db
from pymongo.errors import DuplicateKeyError

def _users_col():
    col = db["users"]
    col.create_index("username", unique=True)
    return col

class UserManager:
    @staticmethod
    def user_exists(username: str) -> bool:
        return _users_col().find_one({"username": username}) is not None

    @staticmethod
    def add_user(username: str, password: str):
        hashed = pbkdf2_sha256.hash(password)
        _users_col().insert_one({
            "username": username,
            "password_hash": hashed,
            "joinedProjects": [],
        })

    @staticmethod
    def login(username: str, password: str) -> bool:
        doc: Optional[dict] = _users_col().find_one({"username": username})
        return bool(doc and pbkdf2_sha256.verify(password, doc["password_hash"]))

    @staticmethod
    def add_project_to_user(username: str, project_id: str) -> None:
        _users_col().update_one(
            {"username": username},
            {"$addToSet": {"joinedProjects": project_id}}
        )

    @staticmethod
    def get_joined_projects(username: str) -> List[str]:
        doc: Optional[dict] = _users_col().find_one(
            {"username": username},
            {"joinedProjects": 1, "_id": 0}
        )
        if not doc:
            return []
        projects = doc.get("joinedProjects")
        if not isinstance(projects, list):
            return []
        return [p for p in projects if isinstance(p, str)]
