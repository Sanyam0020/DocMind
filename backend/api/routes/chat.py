from fastapi import APIRouter

from backend.schemas.chat import (
    AnswerResponse,
    EchoResponse,
    Message,
    Question,
)
from backend.services.chat_service import (
    answer_question,
    echo_message,
)


router = APIRouter()


@router.post("/ask", response_model=AnswerResponse)
def ask_question(payload: Question):
    return answer_question(payload.question)


@router.post("/echo", response_model=EchoResponse)
def echo(payload: Message):
    return echo_message(payload.message)