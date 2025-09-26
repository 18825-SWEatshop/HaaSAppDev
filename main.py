from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import jwt


app = FastAPI()

# Model for login requests
class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/login")
def login(request: LoginRequest):
    # Hardcoded credential check for now
    # TODO: Replace with real authentication 
    
    if request.username == "admin" and request.password == "admin":
        # Generate JWT token 
        token = jwt.encode({"username": request.username}, "this-is-a-super-secret-key-nobody-will-guess-this-key-duck", algorithm="HS256")
        return {"message": "Login successful", "token": token}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")