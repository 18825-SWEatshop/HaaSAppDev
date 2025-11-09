from typing import Optional, List
from passlib.hash import pbkdf2_sha256
from .database import db

def _users_col():
    col = db["users"]
    col.create_index("username_hash", unique=False)
    return col

class UserManager:
    @staticmethod
    def _find_user_doc(username: str) -> Optional[dict]:
        for doc in _users_col().find({}, {"username_hash": 1, "password_hash": 1, "joinedProjects": 1}):
            username_hash = doc.get("username_hash")
            if username_hash and pbkdf2_sha256.verify(username, username_hash):
                return doc
        return None

    @staticmethod
    def user_exists(username: str) -> bool:
        return UserManager._find_user_doc(username) is not None

    @staticmethod
    def add_user(username: str, password: str):
        username_hash = pbkdf2_sha256.hash(username)
        password_hash = pbkdf2_sha256.hash(password)
        _users_col().insert_one({
            "username_hash": username_hash,
            "password_hash": password_hash,
            "joinedProjects": [],
        })

    @staticmethod
    def login(username: str, password: str) -> bool:
        doc = UserManager._find_user_doc(username)
        if not doc:
            return False
        password_hash = doc.get("password_hash")
        return bool(password_hash and pbkdf2_sha256.verify(password, password_hash))

    @staticmethod
    def add_project_to_user(username: str, project_id: str) -> None:
        doc = UserManager._find_user_doc(username)
        if not doc:
            raise ValueError("User not found")
        _users_col().update_one(
            {"_id": doc["_id"]},
            {"$addToSet": {"joinedProjects": project_id}}
        )

    @staticmethod
    def get_joined_projects(username: str) -> List[str]:
        doc = UserManager._find_user_doc(username)
        if not doc:
            return []
        projects = doc.get("joinedProjects")
        if not isinstance(projects, list):
            return []
        return [p for p in projects if isinstance(p, str)]
