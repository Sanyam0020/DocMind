from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.routes import about
from backend.api.routes import chat
from backend.api.routes import documents
from backend.api.routes import health
from backend.core.config import settings


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(about.router)
app.include_router(health.router)
app.include_router(documents.router)
app.include_router(chat.router)


@app.get("/")
def home():
    return {
        "message": "Welcome to DocuMind API"
    }