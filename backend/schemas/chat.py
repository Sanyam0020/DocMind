from pydantic import BaseModel


class Question(BaseModel):
    question: str


class Message(BaseModel):
    message: str


class RetrievedChunk(BaseModel):
    chunk_id: int
    page_number: int
    text: str
    score: float


class AnswerResponse(BaseModel):
    received_question: str
    results: list[RetrievedChunk]


class EchoResponse(BaseModel):
    echo: str