def create_chunks(
    text: str,
    chunk_size: int,
    overlap: int,
    page_number: int
) -> list[dict]:

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")

    if overlap < 0:
        raise ValueError("overlap cannot be negative")

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    words = text.split()

    chunks = []

    step = chunk_size - overlap

    for i in range(0, len(words), step):
        chunk_words = words[i:i + chunk_size]

        if not chunk_words:
            break

        chunk = " ".join(chunk_words)

        chunks.append({
            "chunk_id": len(chunks) + 1,
            "page_number": page_number,
            "text": chunk
        })

        # Stop once we have reached the end of the document.
        if i + chunk_size >= len(words):
            break

    return chunks


if __name__ == "__main__":
    text = "A B C D E F G H I J"

    chunks = create_chunks(
        text=text,
        chunk_size=5,
        overlap=2,
        page_number=1
    )

    for chunk in chunks:
        print(chunk)