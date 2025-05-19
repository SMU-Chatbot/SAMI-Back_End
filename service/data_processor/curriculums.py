import json

def process_curriculums_data():
    with open("Training_Data/curriculums.json", "r", encoding="utf-8") as file:
        curriculums_data = json.load(file)

    documents = []

    for data in curriculums_data:
        major_name = data.get("major", "Unknown Major")

        for curriculum in data.get("curriculums", []):
            curriculum_name = curriculum.get("name", "Unknown Curriculum")
            department = curriculum.get("department", "N/A")
            year = curriculum.get("year", "N/A")
            semester = curriculum.get("semester", "N/A")
            completion = curriculum.get("completion", "N/A")
            credit = curriculum.get("credit", "N/A")

            text = (
                f"전공: {major_name} - 과목명: {curriculum_name} / 학부: {department} "
                f"/ {year}학년 / {semester}학기 / 이수구분: {completion} / {credit}학점"
            )
            documents.append(text)

    return documents
