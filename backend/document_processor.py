from pathlib import Path


def read_document(file_path: Path) -> str:
    return file_path.read_text()


def count_words(text: str) -> int:
    return len(text.split())


def get_first_n_words(text: str, n: int) -> str:
    words = text.split()
    return " ".join(words[:n])


def get_file_size(file_path: Path) -> int:
    return file_path.stat().st_size


def process_document(file_path: Path) -> dict:
    try:
        text = read_document(file_path)

        return {
            "filename": file_path.name,
            "extension": file_path.suffix,
            "word_count": count_words(text),
            "preview": get_first_n_words(text, 10),
            "size_bytes": get_file_size(file_path),
        }

    except FileNotFoundError:
        return {
            "error": f"File not found: {file_path}"
        }


if __name__ == "__main__":
    file_path = Path("data/sample/test.txt")

    document = process_document(file_path)

    print(document)