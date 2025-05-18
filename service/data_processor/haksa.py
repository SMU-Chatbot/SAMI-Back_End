import json

def process_haksa_data():
    with open("Training_Data/Haksa.json", "r", encoding="utf-8") as file:
        haksa_data = json.load(file)

    documents = []
    for item in haksa_data:
        text = f"{item['name']} - 학기: {item['semester']} / 대상: {item['eligibility']} / 기간: {item['period']} / 신청 방법: {item['application']}"
        documents.append(text)
        if item.get("application"):
            text += f" / 신청 방법: {item['application']}"
    return documents