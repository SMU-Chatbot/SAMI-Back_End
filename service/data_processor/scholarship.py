import json

def process_scholarship_data():
    with open("Training_Data/scholarship.json", "r", encoding="utf-8") as file:
        scholarship_data = json.load(file)

    documents = []
    for item in scholarship_data:
        documents.append(
            f"{item['name']} - 대상: {item['eligibility']} / 지원 금액: {item['amount']} / 신청 방법: {item['application']}")
    return documents