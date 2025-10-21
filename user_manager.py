from typing import Optional
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
        _users_col().insert_one({"username": username, "password_hash": hashed})

    @staticmethod
    def login(username: str, password: str) -> bool:
        doc: Optional[dict] = _users_col().find_one({"username": username})
        return bool(doc and pbkdf2_sha256.verify(password, doc["password_hash"]))
