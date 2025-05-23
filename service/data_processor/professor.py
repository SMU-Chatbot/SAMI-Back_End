import json

def process_professor_data():
    with open("Training_Data/professor.json", "r", encoding="utf-8") as file:
        professor_data = json.load(file)

    documents = []

    # 교수 정보 처리
    for item in professor_data:
        text = f"전공: {item['major']}"
        if item.get("name"):
            text += f" / 교수명: {item['name']}"
        if item.get("lab"):
            text += f" / 연구실: {item['lab']}"
        if item.get("phoneNumber"):
            text += f"/ 전화번호: {item['phoneNumber']}"
        if item.get("email"):
            text += f" / 이메일: {item['email']}"
        if item.get("page"):
            text += f" / 페이지: {item['page']}"
        documents.append(text)

    return documents

