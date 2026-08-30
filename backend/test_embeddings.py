# pyrefly: ignore [missing-import]
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


model = SentenceTransformer("all-MiniLM-L6-v2")


sentences = [
    "Machine learning allows computers to learn from data.",
    "Computers can learn patterns from data using machine learning.",
    "The weather is sunny and warm today.",
]


embeddings = model.encode(sentences)


print("Number of sentences:", len(sentences))
print("Embedding shape:", embeddings.shape)


similarity_ab = cosine_similarity(
    [embeddings[0]],
    [embeddings[1]],
)[0][0]


similarity_ac = cosine_similarity(
    [embeddings[0]],
    [embeddings[2]],
)[0][0]


print()
print("Similarity A ↔ B:", similarity_ab)
print("Similarity A ↔ C:", similarity_ac)