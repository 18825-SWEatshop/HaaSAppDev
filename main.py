from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os
from fastapi.middleware.cors import CORSMiddleware
# from dotenv import load_dotenv
from .routers import auth, projects

# load_dotenv()

app = FastAPI()

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(projects.router, prefix="/projects")

# Serve React static files
# dist_path = os.path.join(os.path.dirname(__file__), "dist")
# app.mount("/assets", StaticFiles(directory=os.path.join(dist_path, "assets")), name="assets")

# @app.get("/{full_path:path}")
# async def serve_react(full_path: str):
    # return FileResponse(os.path.join(dist_path, "index.html"))
