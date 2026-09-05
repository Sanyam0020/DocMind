from backend.services.embedding_service import embedding_service
from backend.services.vector_store import VectorStore
from backend.schemas.document import Chunk


def test_vector_store_search():

    texts = [
        "Machine learning allows computers to learn from data.",
        "Supervised learning uses labelled training data.",
        "The weather is sunny and warm today.",
    ]

    embeddings = embedding_service.embed_texts(texts)

    chunks = [
        Chunk(
            document_id="test-document",
            chunk_id=index + 1,
            page_number=1,
            text=text,
            embedding=embedding.tolist(),
        )
        for index, (text, embedding) in enumerate(
            zip(texts, embeddings)
        )
    ]

    store = VectorStore(dimension=384)

    store.add(chunks)

    assert store.count() == 3

    query = "How do computers learn from data?"

    query_embedding = embedding_service.embed_text(query)

    results = store.search(
        query_embedding=query_embedding,
        top_k=2,
    )

    assert len(results) == 2
    assert results[0]["chunk"].chunk_id in [1, 2]