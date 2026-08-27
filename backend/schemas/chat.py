from pydantic import BaseModel


class Question(BaseModel):
    question: str


class Message(BaseModel):
    message: str