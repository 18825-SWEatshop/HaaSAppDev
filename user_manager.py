import hashlib
from typing import Optional, List

from passlib.hash import pbkdf2_sha256
from pymongo.errors import DuplicateKeyError

from .database import db

def _users_col():
    col = db["users"]
    col.create_index("username_digest", unique=True)
    return col

class UserManager:
    @staticmethod
    def _username_digest(username: str) -> str:
        return hashlib.sha256(username.strip().lower().encode("utf-8")).hexdigest()

    @staticmethod
    def _find_user_doc(username: str) -> Optional[dict]:
        digest = UserManager._username_digest(username)
        return _users_col().find_one({"username_digest": digest})

    @staticmethod
    def user_exists(username: str) -> bool:
        return UserManager._find_user_doc(username) is not None

    @staticmethod
    def add_user(username: str, password: str):
        username_hash = pbkdf2_sha256.hash(username)
        password_hash = pbkdf2_sha256.hash(password)
        username_digest = UserManager._username_digest(username)
        try:
            _users_col().insert_one({
                "username_hash": username_hash,
                "username_digest": username_digest,
                "password_hash": password_hash,
                "joinedProjects": [],
            })
        except DuplicateKeyError as exc:
            raise ValueError("Username already exists") from exc

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
