import json

def process_service_data():
    with open("Training_Data/service.json", "r", encoding="utf-8") as file:
        service_data = json.load(file)

    documents = []
    for item in service_data:
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
        if item.get("description"):
            text += f" / {item['description']}"
        if item.get("print_method"):
            text += f" / {item['print_method']}"
        if item.get("refund"):
            text += f" / {item['refund']}"
        if item.get("ratio_A"):
            text += f" / {item['ratio_A']}"
        if item.get("ratio_B"):
            text += f" / {item['ratio_B']}"
        if item.get("confirm"):
            text += f" / {item['confirm']}"
        if item.get("criteria"):
            text += f" / {item['criteria']}"
        if item.get("complain"):
            text += f" / {item['complain']}"

        documents.append(text)
    return documents