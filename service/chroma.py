import chromadb

_COLLECTION_NAMES = [
    "scholarship_knowledge",
    "haksa_knowledge",
    "major_knowledge",
    "ePortfolio_knowledge",
    "facility_knowledge",
    "student_knowledge",
    "double_major_knowledge",
    "graduation_knowledge",
<<<<<<< HEAD
    "service_knowledge",
    "introduction_knowledge",
    "school_knowledge",
=======
    "military_knowledge",
    "service_knowledge",
    "school_knowledge",
    "curriculums_knowledge"
>>>>>>> feature/#12
]

def init_chroma():
    client = chromadb.PersistentClient(path="./chroma_db")
    return client

def init_collections(client):
    collections = {
        name: client.get_or_create_collection(name=name)
        for name in _COLLECTION_NAMES
    }
    return collections