from fastapi import APIRouter, UploadFile, File, HTTPException

from backend.schemas.document import DocumentResponse
from backend.services.ingestion_service import process_document


router = APIRouter()


@router.get("/documents")
def get_documents():
    return {
        "documents": []
    }


@router.post("/documents/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required",
        )

    if not file.filename.lower().endswith(".txt"):
        raise HTTPException(
            status_code=400,
            detail="Only .txt files are supported",
        )

    content = await file.read()

    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400,
            detail="File must be UTF-8 encoded",
        )

    document = process_document(
        document_id=file.filename,
        filename=file.filename,
        extension=".txt",
        size_bytes=len(content),
        text=text,
    )

    return DocumentResponse(
        document_id=document.metadata.document_id,
        filename=document.metadata.filename,
        pages=len(document.pages),
        chunks=len(document.chunks),
    )   