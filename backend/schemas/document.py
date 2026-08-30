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
    chunk_id: int
    page_number: int
    text: str
    embedding: list[float] | None = None


class Document(BaseModel):
    metadata: DocumentMetadata
    pages: list[Page]
    chunks: list[Chunk]