from fastapi import APIRouter

from backend.schemas.document import DocumentResponse
from backend.services.ingestion_service import process_document


router = APIRouter()


@router.get("/documents")
def get_documents():
    return {
        "documents": []
    }


@router.post("/documents/process", response_model=DocumentResponse)
def process_document_route(
    document_id: str,
    filename: str,
    extension: str,
    size_bytes: int,
    text: str,
):
    document = process_document(
        document_id=document_id,
        filename=filename,
        extension=extension,
        size_bytes=size_bytes,
        text=text,
    )

    return DocumentResponse(
        document_id=document.metadata.document_id,
        filename=document.metadata.filename,
        pages=len(document.pages),
        chunks=len(document.chunks),
    )