import json

def process_introduction_data():
    with open("Training_Data/introduction.json", "r", encoding="utf-8") as file:
        introduction_data = json.load(file)

    documents = []
    for item in introduction_data:
        documents.append(
            f"{item['title']} : {item['description']}")
    return documents