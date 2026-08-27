from fastapi import APIRouter

from backend.schemas.chat import Message, Question
from backend.services.chat_service import answer_question


router = APIRouter()


@router.post("/ask")
def ask_question(data: Question):
    return answer_question(data.question)


@router.post("/echo")
def echo(data: Message):
    return {
        "echo": data.message
    }