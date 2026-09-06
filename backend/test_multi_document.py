from backend.schemas.document import Chunk
from backend.services.embedding_service import embedding_service
from backend.services.vector_store import VectorStore


def make_chunk(document_id, chunk_id, text):
    embedding = embedding_service.embed_text(text)

    return Chunk(
        document_id=document_id,
        chunk_id=chunk_id,
        page_number=1,
        text=text,
        embedding=embedding.tolist(),
    )


def test_multiple_documents_are_isolated():

    store = VectorStore(dimension=384)

    document_a = [
        make_chunk(
            "document-a",
            1,
            "DocuMind is an AI document question answering application.",
        ),
        make_chunk(
            "document-a",
            2,
            "DocuMind uses RAG, embeddings, and vector search.",
        ),
    ]

    document_b = [
        make_chunk(
            "document-b",
            1,
            "Smart irrigation uses soil moisture and weather data.",
        ),
        make_chunk(
            "document-b",
            2,
            "The irrigation system uses machine learning.",
        ),
    ]

    store.add(document_a)
    store.add(document_b)

    assert store.count() == 4
    assert len(store.chunks) == 4

    # Remove document A.
    store.remove_document("document-a")

    assert store.count() == 2
    assert len(store.chunks) == 2

    # Only document B should remain.
    assert all(
        chunk.document_id == "document-b"
        for chunk in store.chunks
    )

    # Search should only return document B.
    query_embedding = embedding_service.embed_text(
        "How does smart irrigation work?"
    )

    results = store.search(
        query_embedding=query_embedding,
        top_k=2,
    )

    assert len(results) == 2

    assert all(
        result["chunk"].document_id == "document-b"
        for result in results
    )


def test_reuploading_document_replaces_old_chunks():

    store = VectorStore(dimension=384)

    old_chunks = [
        make_chunk(
            "document-a",
            1,
            "Old document content.",
        )
    ]

    new_chunks = [
        make_chunk(
            "document-a",
            1,
            "Updated document content.",
        ),
        make_chunk(
            "document-a",
            2,
            "More updated document content.",
        ),
    ]

    store.add(old_chunks)

    assert store.count() == 1

    # Simulate the behavior used by ingestion_service.
    store.remove_document("document-a")
    store.add(new_chunks)

    assert store.count() == 2
    assert len(store.chunks) == 2

    assert all(
        chunk.document_id == "document-a"
        for chunk in store.chunks
    )

    assert store.chunks[0].text == "Updated document content."
    assert store.chunks[1].text == "More updated document content."