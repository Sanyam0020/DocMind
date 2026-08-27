def process_document(text: str) -> dict:
    return {
        "status": "processed",
        "characters": len(text),
    }