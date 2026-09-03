from backend.chunking import create_chunks
from backend.schemas.document import (
    Chunk,
    Document,
    DocumentMetadata,
    Page,
)
from backend.core.config import settings
from backend.services.embedding_service import embedding_service
from backend.services.vector_store import vector_store


def process_document(
    document_id: str,
    filename: str,
    extension: str,
    size_bytes: int,
    text: str,
    page_texts: list[str] | None = None,
) -> Document:

    metadata = DocumentMetadata(
        document_id=document_id,
        filename=filename,
        extension=extension,
        size_bytes=size_bytes,
    )

    # For TXT files, use the complete text as one page.
    # For PDFs, page_texts contains one entry per PDF page.
    if page_texts is None:
        page_texts = [text]

    pages = [
        Page(
            page_number=index + 1,
            text=page_text,
        )
        for index, page_text in enumerate(page_texts)
    ]

    chunks = []

    for page in pages:
        if not page.text.strip():
            continue

        page_chunks = create_chunks(
            text=page.text,
            chunk_size=settings.chunk_size,
            overlap=settings.chunk_overlap,
            page_number=page.page_number,
            document_id=document_id,
        )

        chunks.extend(page_chunks)

    if not chunks:
        raise ValueError("No readable text found in the document.")

    texts = [chunk["text"] for chunk in chunks]

    embeddings = embedding_service.embed_texts(texts)

    chunk_objects = []

    for chunk, embedding in zip(chunks, embeddings):
        chunk_objects.append(
            Chunk(
                **chunk,
                embedding=embedding.tolist(),
            )
        )

    vector_store.remove_document(document_id)
    vector_store.add(chunk_objects)

    return Document(
        metadata=metadata,
        pages=pages,
        chunks=chunk_objects,
    )