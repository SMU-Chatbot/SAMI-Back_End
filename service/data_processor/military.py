import json

def process_military_data():
    with open("Training_Data/military.json", "r", encoding="utf-8") as file:
        military_data = json.load(file)

    documents = []
    for item in military_data:
        text = f"{item['title']} / 홈페이지: {item['page']}"
        if item.get("phoneNumber"):
            text += f" / 전화번호: {item['phoneNumber']}"
        if item.get("category"):
            text += f" / 종류: {item['category']}"
        if item.get("method"):
            text += f" / 방법: {item['method']}"
        if item.get("Training_Center"):
            text += f" / 훈련장: {item['Training_Center']}"
        if item.get("transportation"):
            text += f" / 교통수단: {item['transportation']}"
        if item.get("time"):
            text += f" / {item['time']}"
        if item.get("delay"):
            text += f" / {item['delay']}"


        documents.append(text)
    return documents