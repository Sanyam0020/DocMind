from pydantic import BaseModel


class Question(BaseModel):
    question: str


class Message(BaseModel):
    message: str


class AnswerResponse(BaseModel):
    received_question: str


class EchoResponse(BaseModel):
    echo: str