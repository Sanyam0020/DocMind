from sklearn.metrics.pairwise import cosine_similarity


class RetrievalService:

    def retrieve(
        self,
        query_embedding,
        chunks,
        top_k: int = 5,
    ):
        chunk_embeddings = [
            chunk.embedding
            for chunk in chunks
        ]

        similarities = cosine_similarity(
            [query_embedding],
            chunk_embeddings,
        )[0]

        ranked_indices = similarities.argsort()[::-1]

        results = []

        for index in ranked_indices[:top_k]:
            results.append({
                "chunk": chunks[index],
                "score": float(similarities[index]),
            })

        return results


retrieval_service = RetrievalService()