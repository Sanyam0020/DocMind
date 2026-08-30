from backend.services.embedding_service import embedding_service


texts = [
    "Machine learning allows computers to learn from data.",
    "Computers can learn patterns from data using machine learning.",
    "The weather is sunny today.",
]


embeddings = embedding_service.embed_texts(texts)


print("Number of texts:", len(texts))
print("Embedding shape:", embeddings.shape)

for index, embedding in enumerate(embeddings):
    print()
    print("Text:", texts[index])
    print("Vector dimensions:", len(embedding))