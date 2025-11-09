from typing import Optional, List
from pymongo.errors import DuplicateKeyError

from .database import db
from .cipher import encrypt

def _users_col():
    col = db["users"]
    col.create_index("username_cipher", unique=True)
    return col

class UserManager:
    @staticmethod
    def _find_user_doc(username: str) -> Optional[dict]:
        try:
            username_cipher = encrypt(username, 5, 1)
        except ValueError:
            return None
        return _users_col().find_one({"username_cipher": username_cipher})

    @staticmethod
    def user_exists(username: str) -> bool:
        return UserManager._find_user_doc(username) is not None

    @staticmethod
    def add_user(username: str, password: str):
        try:
            username_cipher = encrypt(username, 5, 1)
        except ValueError as exc:
            raise ValueError("Invalid characters in username") from exc
        try:
            password_cipher = encrypt(password, 5, 1)
        except ValueError as exc:
            raise ValueError("Invalid characters in password") from exc
        try:
            _users_col().insert_one({
                "username_cipher": username_cipher,
                "password_cipher": password_cipher,
                "joinedProjects": [],
            })
        except DuplicateKeyError as exc:
            raise ValueError("Username already exists") from exc

    @staticmethod
    def login(username: str, password: str) -> bool:
        doc = UserManager._find_user_doc(username)
        if not doc:
            return False
        password_cipher = doc.get("password_cipher")
        try:
            candidate_cipher = encrypt(password, 5, 1)
        except ValueError:
            return False
        return bool(password_cipher and password_cipher == candidate_cipher)

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
