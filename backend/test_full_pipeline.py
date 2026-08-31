from backend.services.ingestion_service import process_document
from backend.services.chat_service import answer_question
from backend.services.vector_store import vector_store


text = """
DocuMind is a document question answering system.

It uses retrieval augmented generation to answer questions.

Documents are processed into smaller chunks.

Machine learning allows computers to learn from data.
"""


print("Processing document...")

document = process_document(
    document_id="test-123",
    filename="test.txt",
    extension=".txt",
    size_bytes=len(text.encode("utf-8")),
    text=text,
)


print("Document processed.")
print("Chunks:", len(document.chunks))
print("Vectors stored:", vector_store.count())

print()


question = "What is DocuMind?"

print("Question:", question)

result = answer_question(question)

print("Results:", len(result["results"]))

print()

for item in result["results"]:
    print("Chunk ID:", item["chunk_id"])
    print("Page:", item["page_number"])
    print("Score:", item["score"])
    print("Text:", item["text"])
    print()