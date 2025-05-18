import json

def process_school_data():
    with open("Training_Data/school.json", "r", encoding="utf-8") as file:
        school_data = json.load(file)

    documents = []
    for item in school_data:
        documents.append(
            f"{item['title']}\n {item['description']} / 위치: {item['location']} / 전화번호: {item['phoneNumber']} / 홈페이지: {item['page']}")
    return documents