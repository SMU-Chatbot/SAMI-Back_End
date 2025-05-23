import json

def process_curriculums_data():
    with open("Training_Data/curriculums.json", "r", encoding="utf-8") as file:
        curriculums_data = json.load(file)

    documents = []

    for data in curriculums_data:
        major = data["name"]  # 전공과목
        curriculums = data["curriculums"]  # 전공과목 교육과정

        documents.append(f"{major} / 교육과정: {curriculums}")

    return documents
