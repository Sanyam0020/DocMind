from pathlib import Path


file_path = Path("data/sample/test.txt")

text = file_path.read_text()

print(text)