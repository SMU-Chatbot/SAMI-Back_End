import json

def process_major_data():
    with open("Training_Data/majors.json", "r", encoding="utf-8") as file:
        major_data = json.load(file)

    documents = []

    # 전공과목과 교수 정보를 처리합니다.
    for major in major_data:
        major_name = major["name"]  # 전공과목 이름
        major_phone = major["phoneNumber"]  # 전공과목 전화번호
        major_fax = major["fax"]
        major_office = major["office"]
        major_page = major["page"]  # 전공과목 홈페이지

        # 전공과목 정보 추가
        documents.append(f"전공: {major_name} - 전화번호: {major_phone} / 팩스: {major_fax} / 학과 사무실: {major_office} / 홈페이지: {major_page}")

    return documents

