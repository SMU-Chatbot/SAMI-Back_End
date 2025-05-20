from service.data_processor import *

def load_data_to_chroma(embedding_model, collections):

    collections_with_data = {
        "scholarship": (collections["scholarship_knowledge"], process_scholarship_data()),
        "haksa": (collections["haksa_knowledge"], process_haksa_data()),
        "major": (collections["major_knowledge"], process_major_data()),
        "facility": (collections["facility_knowledge"], process_facility_data()),
        "student": (collections["student_knowledge"], process_student_data()),
        "double_major": (collections["double_major_knowledge"], process_double_major_data()),
        "graduation": (collections["graduation_knowledge"], process_graduation_data()),
        "service": (collections["service_knowledge"], process_service_data()),
        "introduction": (collections["introduction_knowledge"], process_introduction_data()),
        "school": (collections["school_knowledge"], process_school_data()),
        "military": (collections["military_knowledge"], process_military_data()),
        "service": (collections["service_knowledge"], process_service_data()),
        "school": (collections["school_knowledge"], process_school_data()),
        "curriculums": (collections["curriculums_knowledge"], process_curriculums_data())
    }

    for category, (collection, data) in collections_with_data.items():
        if collection.count() == 0:
            print(f"{category} 데이터 저장 중...")
            for idx, text in enumerate(data):
                embedding = embedding_model.encode(text).tolist()
                collection.add(ids=[f"{category}_{idx}"], embeddings=[embedding], metadatas=[{"text": text}])
            print(f"{category} 데이터 저장 완료!")


def query_chroma_collections(user_embedding, collections):
    counts = len(user_embedding)

    category_texts = {}
    for category, collection in collections.items():
        results = collection.query(query_embeddings=[user_embedding], n_results=counts)
        docs = [doc["text"] for doc in results["metadatas"][0] if "text" in doc]
        category_texts[category] = "\n\n".join(docs)

    return category_texts