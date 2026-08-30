# pyrefly: ignore [missing-import]
from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"


class EmbeddingService:

    def __init__(self):
        self.model = SentenceTransformer(MODEL_NAME)

    def embed_text(self, text: str):
        return self.model.encode(text)

    def embed_texts(self, texts: list[str]):
        return self.model.encode(texts)


embedding_service = EmbeddingService()