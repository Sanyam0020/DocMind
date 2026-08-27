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
def process_document_route(text: str):
    return process_document(text)