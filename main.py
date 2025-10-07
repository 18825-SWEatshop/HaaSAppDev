from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import jwt
from .user_manager import UserManager

secret_key = "this-is-a-super-secret-key-nobody-will-guess-this-key-duck"
app = FastAPI()

# Model for login requests
class LoginRequest(BaseModel):
    username: str
    password: str



@app.post("/login")
def login(request: LoginRequest):
    if UserManager.login(request.username, request.password):
        token = jwt.encode({"username": request.username}, secret_key, algorithm="HS256")
        return {"message": "Login successful", "token": token}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
@app.post("/register")
def register(request: LoginRequest):
    # Check to see if user already exists
    if UserManager.user_exists(request.username):
        raise HTTPException(status_code=401, detail="User already exists")
    
    # Add user to user manager
    user = UserManager.add_user(request.username, request.password)

    # Create jwt for user and return it
    token = jwt.encode({"username": user["username"]}, secret_key, algorithm="HS256")
    return {"message": "User registered successfully", "token": token}
