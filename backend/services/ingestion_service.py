from backend.chunking import create_chunks
from backend.schemas.document import (
    Chunk,
    Document,
    DocumentMetadata,
    Page,
)
from backend.core.config import settings


def process_document(
    document_id: str,
    filename: str,
    extension: str,
    size_bytes: int,
    text: str,
) -> Document:

    metadata = DocumentMetadata(
        document_id=document_id,
        filename=filename,
        extension=extension,
        size_bytes=size_bytes,
    )

    pages = [
        Page(
            page_number=1,
            text=text,
        )
    ]

    chunks = []

    for page in pages:

        page_chunks = create_chunks(
            text=page.text,
            chunk_size=settings.chunk_size,
            overlap=settings.chunk_overlap,
            page_number=page.page_number,
        )

        chunks.extend(page_chunks)

    chunk_objects = [
        Chunk(**chunk)
        for chunk in chunks
    ]

    return Document(
        metadata=metadata,
        pages=pages,
        chunks=chunk_objects,
    )