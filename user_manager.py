# Static set of users for now, will later be replaced with DB

users = {
    "alice": "password123",
    "bob": "securepassword",
    "charlie": "mypassword",
    }
class UserManager:
    @staticmethod
    def user_exists(username: str, password: str) -> bool:
        # Check to see if the user exists in the existing users
        for user, pwd in users.items():
            if user == username and pwd == password:
                return True
        return False

    @staticmethod
    def add_user(username: str, password: str) -> dict:
        users[username] = password
        print(f"Current users: {users}")
        return {"username": username, "password": password}