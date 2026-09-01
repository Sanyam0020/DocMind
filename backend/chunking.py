def create_chunks(
    text: str,
    chunk_size: int,
    overlap: int,
    page_number: int,
    document_id: str,
) -> list[dict]:

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")

    if overlap < 0:
        raise ValueError("overlap cannot be negative")

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    words = text.split()

    if not words:
        return []

    chunks = []

    step = chunk_size - overlap

    for start in range(0, len(words), step):
        end = start + chunk_size
        chunk_words = words[start:end]

        if not chunk_words:
            break

        chunks.append(
            {
                "document_id": document_id,
                "chunk_id": len(chunks) + 1,
                "page_number": page_number,
                "text": " ".join(chunk_words),
            }
        )

        if end >= len(words):
            break

    return chunks


if __name__ == "__main__":
    text = (
        "A B C D E F G H I J "
        "K L M N O P Q R S T "
        "U V W X Y Z"
    )

    chunks = create_chunks(
        text=text,
        chunk_size=10,
        overlap=2,
        page_number=1,
        document_id="test-123",
    )

    for chunk in chunks:
        print(chunk)