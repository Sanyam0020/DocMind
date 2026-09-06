import json
from pathlib import Path

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

    def add(self, chunks: list[Chunk]):
        """Add chunks and their embeddings to the vector store."""

        if not chunks:
            return

        embeddings = np.asarray(
            [chunk.embedding for chunk in chunks],
            dtype="float32",
        )

        if embeddings.ndim != 2:
            raise ValueError("Embeddings must be a 2D array.")

        if embeddings.shape[1] != self.dimension:
            raise ValueError(
                f"Embedding dimension mismatch: "
                f"expected {self.dimension}, "
                f"got {embeddings.shape[1]}"
            )

        self.index.add(embeddings)
        self.chunks.extend(chunks)

    def search(
        self,
        query_embedding: np.ndarray,
        top_k: int = 5,
    ):
        """Search for the most similar chunks."""

        if self.index.ntotal == 0:
            return []

        query_embedding = np.asarray(
            [query_embedding],
            dtype="float32",
        )

        if query_embedding.shape[1] != self.dimension:
            raise ValueError(
                f"Query embedding dimension mismatch: "
                f"expected {self.dimension}, "
                f"got {query_embedding.shape[1]}"
            )

        top_k = min(top_k, self.index.ntotal)

        scores, indices = self.index.search(
            query_embedding,
            top_k,
        )

        results = []

        for score, index in zip(scores[0], indices[0]):

            if index == -1:
                continue

            results.append(
                {
                    "chunk": self.chunks[index],
                    "score": float(score),
                }
            )

        return results

    def count(self) -> int:
        """Return the number of stored vectors."""

        return self.index.ntotal

    def save(self, path: str):
        """
        Save the FAISS index and the corresponding chunks.

        FAISS stores vectors, but it does not store the Chunk objects.
        Therefore the chunks are persisted in a companion JSON file.
        """

        index_path = Path(path)
        chunks_path = Path(f"{path}.chunks.json")

        if len(self.chunks) != self.index.ntotal:
            raise RuntimeError(
                "Vector store is inconsistent: "
                f"{self.index.ntotal} vectors but "
                f"{len(self.chunks)} chunks."
            )

        faiss.write_index(self.index, str(index_path))

        chunks_data = [
            chunk.model_dump()
            for chunk in self.chunks
        ]

        chunks_path.write_text(
            json.dumps(chunks_data, ensure_ascii=False),
            encoding="utf-8",
        )

    def load(self, path: str):
        """
        Load the FAISS index and corresponding chunks.
        """

        index_path = Path(path)
        chunks_path = Path(f"{path}.chunks.json")

        if not index_path.exists():
            raise FileNotFoundError(
                f"FAISS index not found: {index_path}"
            )

        if not chunks_path.exists():
            raise FileNotFoundError(
                f"Chunk metadata not found: {chunks_path}"
            )

        index = faiss.read_index(str(index_path))

        if index.d != self.dimension:
            raise ValueError(
                f"Index dimension mismatch: "
                f"expected {self.dimension}, "
                f"got {index.d}"
            )

        chunks_data = json.loads(
            chunks_path.read_text(encoding="utf-8")
        )

        chunks = [
            Chunk.model_validate(chunk)
            for chunk in chunks_data
        ]

        if index.ntotal != len(chunks):
            raise RuntimeError(
                "Loaded vector store is inconsistent: "
                f"{index.ntotal} vectors but "
                f"{len(chunks)} chunks."
            )

        self.index = index
        self.chunks = chunks


vector_store = VectorStore(dimension=384)