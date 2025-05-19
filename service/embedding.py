from sentence_transformers import SentenceTransformer

def load_embedding_model(model_name = "sentence-transformers/all-MiniLM-L6-v2"):
    return SentenceTransformer(model_name)