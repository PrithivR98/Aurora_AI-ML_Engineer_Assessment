from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.api import router as api_router

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# frontend
@app.get("/")
def read_root():
    return FileResponse("app/static/index.html")

# API
app.include_router(api_router)
