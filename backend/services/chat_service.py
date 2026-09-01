from backend.core.config import settings
from backend.services.embedding_service import embedding_service
from backend.services.vector_store import vector_store
from backend.services.llm_service import llm_service


def answer_question(question: str) -> dict:

    query_embedding = embedding_service.embed_text(question)

    results = vector_store.search(
        query_embedding=query_embedding,
        top_k=settings.top_k,
    )

    context = "\n\n".join(
        result["chunk"].text
        for result in results
    )

    answer = llm_service.generate(
        question=question,
        context=context,
    )

    return {
        "received_question": question,
        "answer": answer,
        "results": [
            {
                "chunk_id": result["chunk"].chunk_id,
                "page_number": result["chunk"].page_number,
                "text": result["chunk"].text,
                "score": result["score"],
            }
            for result in results
        ],
    }


def echo_message(message: str) -> dict:
    return {
        "echo": message
    }