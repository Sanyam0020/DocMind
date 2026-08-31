from pathlib import Path

from backend.services.embedding_service import embedding_service
from backend.services.vector_store import VectorStore
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


store = VectorStore(dimension=384)
store.add(chunks)

path = "backend/test_index.faiss"

store.save(path)

print("Saved vectors:", store.count())


loaded_store = VectorStore(dimension=384)
loaded_store.load(path)

print("Loaded vectors:", loaded_store.count())


Path(path).unlink()

print("Persistence test passed.")