from backend.services.ingestion_service import process_document


text = """
DocuMind is a document question answering system.

It uses retrieval augmented generation to answer questions.

Documents are processed into smaller chunks.
"""


document = process_document(
    document_id="test-123",
    filename="test.txt",
    extension=".txt",
    size_bytes=100,
    text=text,
)


print("Document ID:", document.metadata.document_id)
print("Filename:", document.metadata.filename)
print("Pages:", len(document.pages))
print("Chunks:", len(document.chunks))

for chunk in document.chunks:

    print()
    print("Chunk ID:", chunk.chunk_id)
    print("Page:", chunk.page_number)
    print("Text:", chunk.text)
    print("Embedding dimensions:", len(chunk.embedding))
    print("First 5 values:", chunk.embedding[:5])