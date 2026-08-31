from backend.services.embedding_service import embedding_service
from backend.services.retrieval_service import retrieval_service
from backend.schemas.document import Chunk


texts = [
    "Machine learning allows computers to learn from data.",
    "Supervised learning uses labelled training data.",
    "The weather is sunny and warm today.",
]


embeddings = embedding_service.embed_texts(texts)


chunks = [
    Chunk(
        chunk_id=index + 1,
        page_number=1,
        text=text,
        embedding=embedding.tolist(),
    )
    for index, (text, embedding) in enumerate(
        zip(texts, embeddings)
    )
]


query = "How do computers learn from data?"

query_embedding = embedding_service.embed_text(query)


results = retrieval_service.retrieve(
    query_embedding=query_embedding,
    chunks=chunks,
    top_k=3,
)


print("Query:", query)
print()

for result in results:

    chunk = result["chunk"]
    score = result["score"]

    print("Chunk ID:", chunk.chunk_id)
    print("Page:", chunk.page_number)
    print("Score:", score)
    print("Text:", chunk.text)
    print()