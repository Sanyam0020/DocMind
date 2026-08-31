from pydantic import BaseModel


class DocumentMetadata(BaseModel):
    document_id: str
    filename: str
    extension: str
    size_bytes: int


class Page(BaseModel):
    page_number: int
    text: str


class Chunk(BaseModel):
    document_id: str
    chunk_id: int
    page_number: int
    text: str
    embedding: list[float]


class Document(BaseModel):
    metadata: DocumentMetadata
    pages: list[Page]
    chunks: list[Chunk]


class DocumentResponse(BaseModel):
    document_id: str
    filename: str
    pages: int
    chunks: int