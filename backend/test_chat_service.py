from backend.schemas.document import Chunk
from backend.services.embedding_service import embedding_service
from backend.services.vector_store import vector_store
from backend.services.chat_service import answer_question


texts = [
    "Machine learning allows computers to learn from data.",
    "Supervised learning uses labelled training data.",
    "The weather is sunny and warm today.",
]


chunks = []

for i, text in enumerate(texts):

    embedding = embedding_service.embed_text(text)

    chunks.append(
        Chunk(
            document_id="test-123",
            chunk_id=i + 1,
            page_number=1,
            text=text,
            embedding=embedding.tolist(),
        )
    )


vector_store.add(chunks)


result = answer_question(
    "How do computers learn from data?"
)


print("Question:")
print(result["received_question"])

print()

print("Number of results:", len(result["results"]))

print()

for item in result["results"]:

    print("Chunk ID:", item["chunk_id"])
    print("Page:", item["page_number"])
    print("Score:", item["score"])
    print("Text:", item["text"])
    print()