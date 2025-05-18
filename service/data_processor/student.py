import json

def process_student_data():
    with open("Training_Data/student.json", "r", encoding="utf-8") as file:
        student_data = json.load(file)

    documents = []

    # 학적 정보를 처리
    for student in student_data:
        student_name = student["title"] # 학적
        student_pNumber = student["phoneNumber"] # 학사운영팀 번호
        student_page = student["page"] # 학적 관련 페이지

        # 학사 정보 추가
        documents.append(f"{student_name} / 학사운영팀 전화번호: {student_pNumber} / 홈페이지: {student_page}")

        # 학적 처리
        for item in student["student"]:
            text = f"{item['title']}"
            # 휴학
            if item["title"] == "휴학":
                text += f"문의 전화번호: {item.get('phoneNumber')}\n"
                text += f"홈페이지: {item.get('page')}\n"
                text += f"신청 방법: {item.get('method')}\n"
                text += f"신청 기간: {item.get('period')}\n"
                text += f"\n휴학 유형별 정보:\n"

                for t in item.get("types", []):
                    text += f"\n- {t['type']}\n"
                    text += f"  설명: {t['description']}\n"
                    text += f"  기간: {t['duration']}\n"
                    if t.get("required_documents"):
                        text += f"  제출서류: {t['required_documents']}\n"
                    if t.get("eligibility"):
                        text += f"  신청 자격: {t['eligibility']}\n"
                    if t.get("note"):
                        text += f"  비고: {t['note']}\n"
            # 복학
            if item["title"] == "복학":

                text += f"문의 전화번호: {item.get('phoneNumber')}\n"
                text += f"홈페이지: {item.get('page')}\n"
                text += f"신청 방법: {item.get('method')}\n"
                text += f"신청 기간: {item.get('period')}\n"

                required_docs = item.get("required_documents", {})
                if required_docs:
                    text += f"\n복학 유형별 제출서류:\n"
                    if "general_leave" in required_docs:
                        text += f"- 일반휴학: {required_docs['general_leave']}\n"
                    if "military_leave" in required_docs:
                        text += f"- 군휴학: {required_docs['military_leave']}\n"
                    if "startup_leave" in required_docs:
                        text += f"- 창업휴학: {required_docs['startup_leave']}\n"
                if item.get("notes"):
                    text += f"\n유의사항: {item['notes']}\n"
            # 전과
            if item["title"] == "전과":
                text += f"전화번호 문의: {item.get('phoneNumber')}\n"
                text += f"홈페이지: {item.get('page')}\n"
                text += f"신청 방법: {item.get('method')}\n"
                text += f"신청 기간: {item.get('period')}\n"

                if item.get("major_transfer"):
                    text += f"\n캠퍼스 내 전과:\n- {item['major_transfer']}\n"

                if item.get("campus_transfer"):
                    text += f"\n캠퍼스 간 전과:\n- {item['campus_transfer']}\n"

            # 전과
            if item["title"] == "제적 및 자퇴":
                text += f"종류: {item.get('category')}\n"
                text += f"신청 방법: {item.get('method')}\n"
                text += f"전화번호 문의: {item.get('phoneNumber')}\n"
                text += f"홈페이지: {item.get('page')}\n"



            # 증명서 발급
            if item["title"] == "증명서 발급":
                text += f"문의: {item.get('phoneNumber')}\n"
                text += f"홈페이지: {item.get('page')}\n"

            documents.append(text)

    return documents