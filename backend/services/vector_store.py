# pyrefly: ignore [missing-import]
import faiss
import numpy as np

from backend.schemas.document import Chunk


class VectorStore:

    def __init__(self, dimension: int):
        self.dimension = dimension
        self.index = faiss.IndexFlatIP(dimension)
        self.chunks: list[Chunk] = []
            
    def remove_document(self, document_id: str):
        """Remove all chunks belonging to a document."""
        remaining_chunks = [
            chunk
            for chunk in self.chunks
            if chunk.document_id != document_id
        ]

        if len(remaining_chunks) == len(self.chunks):
            return

        self.index = faiss.IndexFlatIP(self.dimension)

        if remaining_chunks:
            embeddings = np.asarray(
                [chunk.embedding for chunk in remaining_chunks],
                dtype="float32",
            )
            self.index.add(embeddings)

        self.chunks = remaining_chunks
        
    def add(
        self,
        chunks: list[Chunk],
    ):
        embeddings = np.asarray(
            [chunk.embedding for chunk in chunks],
            dtype="float32",
        )

        self.index.add(embeddings)
        self.chunks.extend(chunks)

    def search(
        self,
        query_embedding: np.ndarray,
        top_k: int = 5,
    ):
        query_embedding = np.asarray(
            [query_embedding],
            dtype="float32",
        )

        scores, indices = self.index.search(
            query_embedding,
            top_k,
        )

        results = []

        for score, index in zip(scores[0], indices[0]):

            if index == -1:
                continue

            results.append({
                "chunk": self.chunks[index],
                "score": float(score),
            })

        return results

    def count(self) -> int:
        return self.index.ntotal

    def save(self, path: str):
        faiss.write_index(self.index, path)


    def load(self, path: str):
        self.index = faiss.read_index(path)    


vector_store = VectorStore(dimension=384)