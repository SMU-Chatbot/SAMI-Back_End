import json

def process_graduation_data():
    with open("Training_Data/graduation.json", "r", encoding="utf-8") as file:
        graduation_data = json.load(file)

    documents = []
    for item in graduation_data:
        documents.append(
            f"{item['name']} - 학점: {item['grade']} / 학기: {item['semester']} / 평점 평균: {item['GPA']} / 전화번호: {item['phoneNumber']} / {item['note']} / 홈페이지: {item['page']}")
    return documents