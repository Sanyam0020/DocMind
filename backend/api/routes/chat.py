from fastapi import APIRouter

from backend.schemas.chat import Message, Question


router = APIRouter()


@router.post("/ask")
def ask_question(data: Question):
    return {
        "received_question": data.question
    }


@router.post("/echo")
def echo(data: Message):
    return {
        "echo": data.message
    }