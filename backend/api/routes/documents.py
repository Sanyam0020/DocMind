from fastapi import APIRouter, UploadFile, File, HTTPException
# pyrefly: ignore [missing-import]
from pypdf import PdfReader

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

    filename = file.filename
    extension = filename.lower().rsplit(".", 1)[-1]

    content = await file.read()

    if extension == "txt":
        try:
            text = content.decode("utf-8")
        except UnicodeDecodeError:
            raise HTTPException(
                status_code=400,
                detail="TXT file must be UTF-8 encoded",
            )

    elif extension == "pdf":
        try:
            import io

            reader = PdfReader(io.BytesIO(content))

            pages_text = []

            for page in reader.pages:
                page_text = page.extract_text() or ""
                pages_text.append(page_text)

            text = "\n\n".join(pages_text)

        except Exception as exc:
            raise HTTPException(
                status_code=400,
                detail=f"Could not read PDF: {exc}",
            )

        if not text.strip():
            raise HTTPException(
                status_code=400,
                detail="PDF contains no extractable text",
            )

    else:
        raise HTTPException(
            status_code=400,
            detail="Only .txt and .pdf files are supported",
        )

    document = process_document(
        document_id=filename,
        filename=filename,
        extension=f".{extension}",
        size_bytes=len(content),
        text=text,
    )

    return DocumentResponse(
        document_id=document.metadata.document_id,
        filename=document.metadata.filename,
        pages=len(document.pages),
        chunks=len(document.chunks),
    )