from pydantic import BaseModel


class DocumentResponse(BaseModel):
    status: str
    characters: int