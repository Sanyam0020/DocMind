from backend.services.ingestion_service import process_document
from backend.services.chat_service import answer_question


document_text = """
DocuMind is a document question answering system.
It uses retrieval augmented generation to answer questions.
Documents are processed into smaller chunks.

Machine learning allows computers to learn from data.
Supervised learning uses labelled training data.

The weather is sunny and warm today.
"""


print("Processing document...")

document = process_document(
    document_id="test-chat-123",
    filename="test.txt",
    extension=".txt",
    size_bytes=len(document_text.encode("utf-8")),
    text=document_text,
)

print("Document processed.")
print("Chunks stored:", len(document.chunks))


question = "How do computers learn from data?"

print("\nQuestion:")
print(question)

response = answer_question(question)

print("\nAnswer:")
print(response["answer"])

print("\nNumber of results:")
print(len(response["results"]))

for result in response["results"]:
    print("\nChunk ID:", result["chunk_id"])
    print("Page:", result["page_number"])
    print("Score:", result["score"])
    print("Text:", result["text"])