from backend.core.config import settings


print("Application:", settings.app_name)
print("Version:", settings.app_version)
print("Chunk size:", settings.chunk_size)
print("Chunk overlap:", settings.chunk_overlap)
print("Top K:", settings.top_k)