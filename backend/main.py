from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

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
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")