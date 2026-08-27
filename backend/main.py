from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


class Question(BaseModel):
    question: str


class Message(BaseModel):
    message: str    


@app.get("/")
def home():
    return {
        "message": "Welcome to DocuMind API"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "DocuMind API",
        "version": "0.1.0"
    }


@app.post("/ask")
def ask_question(data: Question):
    return {
        "received_question": data.question
    }   

@app.post("/chat")
def chat(data: Message):
    return {
        "echo": data.message
    }   

@app.get("/documents")
def get_documents():
    return {
        "documents": []
    }

@app.get("/about")
def about():
    return {
        "version": "1.0.0",
        "name": "DocuMind",
        "description": "A simple RAG application",
        "author": "Sanyam"
    }