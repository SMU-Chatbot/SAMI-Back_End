import json

def process_double_major_data():
    with open("Training_Data/double_major.json", "r", encoding="utf-8") as file:
        double_major_data = json.load(file)

    documents = []
    for item in double_major_data:
        text = f"{item['name']} - "
        documents.append(text)

        types = item.get("type", [{}])[0]
        for t_name, t_desc in types.items():
            documents.append(f"종류 \n{t_name}: {t_desc}")
        documents.append(
            f"신청 방법: {item['method']} / 신청 기간: {item['period']} / 전화번호: {item['phoneNumber']} / 홈페이지: {item['page']}"
        )

    return documents