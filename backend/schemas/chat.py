from pydantic import BaseModel, field_validator


class Question(BaseModel):
    question: str

    @field_validator("question")
    @classmethod
    def question_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Question cannot be empty.")

        return value


class Message(BaseModel):
    message: str


class RetrievedChunk(BaseModel):
    chunk_id: int
    page_number: int
    text: str
    score: float


class AnswerResponse(BaseModel):
    received_question: str
    answer: str
    results: list[RetrievedChunk]


class EchoResponse(BaseModel):
    echo: str