import json

def process_ePortfolio_data():
    with open("Training_Data/smcareer_seoul_25.json", "r", encoding="utf-8") as file:
        ePortfolio_data = json.load(file)

    documents = []

    for item in ePortfolio_data:
        documents.append(
            f"{item['title']} - 링크: {item['url']} / 기간: {item['period']} / 캠퍼스: {item['campus']}"
        )
    return documents