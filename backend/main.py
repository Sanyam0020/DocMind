from fastapi import FastAPI

from backend.api.routes import about
from backend.api.routes import chat
from backend.api.routes import documents
from backend.api.routes import health


app = FastAPI()


app.include_router(about.router)
app.include_router(health.router)
app.include_router(documents.router)
app.include_router(chat.router)


@app.get("/")
def home():
    return {
        "message": "Welcome to DocuMind API"
    }