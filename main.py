from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import chromadb
from sentence_transformers import SentenceTransformer
import json
import os


os.environ["TOKENIZERS_PARALLELISM"] = "false"

# 환경 변수 로드
load_dotenv()
api_key = "api_key"

# Flask 애플리케이션 초기화
app = Flask(__name__)
CORS(app)
client = OpenAI(api_key=api_key)

with open("sami_prompt.txt", "r", encoding="utf-8") as file:
    sami_prompt = file.read()

# Hugging Face 임베딩 모델 로드
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# ChromaDB 초기화 (Persistent 모드)
chroma_client = chromadb.PersistentClient(path="./chroma_db")
# collection = chroma_client.get_or_create_collection(name="knowledge_base")

# 데이터 유형별 컬렉션 생성
scholarship_collection = chroma_client.get_or_create_collection(name="scholarship_knowledge")
haksa_collection = chroma_client.get_or_create_collection(name="haksa_knowledge")
major_collection = chroma_client.get_or_create_collection(name="major_knowledge")
ePortfolio_collection = chroma_client.get_or_create_collection(name="ePortfolio_knowledge")
facility_collection = chroma_client.get_or_create_collection(name="facility_knowledge")
student_collection = chroma_client.get_or_create_collection(name="student_knowledge")
double_major_collection = chroma_client.get_or_create_collection(name="double_major_knowledge")
graduation_collection = chroma_client.get_or_create_collection(name="graduation_knowledge")
service_collection = chroma_client.get_or_create_collection(name="service_knowledge")
introduction_collection = chroma_client.get_or_create_collection(name="introduction_knowledge")
school_collection = chroma_client.get_or_create_collection(name="school_knowledge")

def process_scholarship_data():
    with open("scholarship.json", "r", encoding="utf-8") as file:
        scholarship_data = json.load(file)

    documents = []
    for item in scholarship_data:
        documents.append(
            f"{item['name']} - 대상: {item['eligibility']} / 지원 금액: {item['amount']} / 신청 방법: {item['application']}")
    return documents

def process_graduation_data():
    with open("graduation.json", "r", encoding="utf-8") as file:
        graduation_data = json.load(file)

    documents = []
    for item in graduation_data:
        documents.append(
            f"{item['name']} - 학점: {item['grade']} / 학기: {item['semester']} / 평점 평균: {item['GPA']} / 전화번호: {item['phoneNumber']} / {item['note']} / 홈페이지: {item['page']}")
    return documents

def process_service_data():
    with open("service.json", "r", encoding="utf-8") as file:
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

        documents.append(text)
    return documents

def process_introduction_data():
    with open("introduction.json", "r", encoding="utf-8") as file:
        introduction_data = json.load(file)

    documents = []
    for item in introduction_data:
        documents.append(
            f"{item['title']} : {item['description']}")
    return documents

def process_school_data():
    with open("school.json", "r", encoding="utf-8") as file:
        school_data = json.load(file)

    documents = []
    for item in school_data:
        documents.append(
            f"{item['title']}\n {item['description']} / 위치: {item['location']} / 전화번호: {item['phoneNumber']} / 홈페이지: {item['page']}")
    return documents

def process_haksa_data():
    with open("Haksa.json", "r", encoding="utf-8") as file:
        haksa_data = json.load(file)

    documents = []
    for item in haksa_data:
        text = f"{item['name']} - 학기: {item['semester']} / 대상: {item['eligibility']} / 기간: {item['period']} / 신청 방법: {item['application']}"
        documents.append(text)
        if item.get("application"):
            text += f" / 신청 방법: {item['application']}"
    return documents

def process_major_data():
    with open("majors.json", "r", encoding="utf-8") as file:
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

        # 교수 정보 처리
        for item in major["faculty"]:
            text = f"전공: {major_name} - 교수명: {item['name']} / 연구실: {item['lab']} / 전화번호: {item['phoneNumber']}"
            if item.get("email"):
                text += f" / 이메일: {item['email']}"
            documents.append(text)
    return documents

def process_student_data():
    with open("student.json", "r", encoding="utf-8") as file:
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


def process_facility_data():
    with open("facility.json", "r", encoding="utf-8") as file:
        facility_data = json.load(file)

    documents = []

    # 캠퍼스맵
    for facility in facility_data:
        facility_name = facility["location"]  # 캠퍼스맵
        facility_page = facility["page"]  # 캠퍼스맵 페이지

        # 정보 추가
        documents.append(f"지도: {facility_name}  / 홈페이지: {facility_page}")

        # 정보 처리
        for item in facility["facility"]:
            text = f"{facility_name} - {facility_page} /  {item['title']}"

            if item["title"] in ["학술정보관", "도서관"]:
                text += " / " + " / ".join(
                    filter(None, [
                        f"팩스: {item.get('fax')}",
                        f"번호: {item.get('phoneNumber')}",
                        f"운영시간: {item.get('Library time')}",
                        f"참고정간실: {item.get('reference room')}",
                        f"열람실 1: {item.get('study room 1 time')}",
                        f"열람실 2: {item.get('study room 2 time')}",
                        f"리딩라운지: {item.get('reading Lounge')}",
                        f"대출 규정: {item.get('Library Loan')}",
                        f"열람실 이용자: {item.get('study room reservation user')}",
                        f"열람실 예약 방법: {item.get('study room reservation guide')}",
                        f"열람실 이용 시간: {item.get('study room reservation time')}",
                        f"열람실 자리배정시스템 위치: {item.get('study room reservation Kiosk')}",
                        f"세미나실 예약: {item.get('Seminar Room reservation 1')}",
                        f"세미나실 예약(앱): {item.get('Seminar Room reservation 2')}",
                        f"홈페이지: {item.get('page')}"
                    ])
                )

            if item.get("fax"):
                text += f" / 팩스: {item['fax']}"
            if item.get("phoneNumber"):
                text += f" / 번호: {item['phoneNumber']}"
            if item.get("time"):
                text += f" / 시간: {item['time']}"
            if item.get("open"):
                text += f" / 개방: {item['open']}"
            if item.get("close"):
                text += f" / 마감: {item['close']}"
            if item.get("location"):
                text += f" / 위치: {item['location']}"
            if item.get("email"):
                text += f" / 이메일: {item['email']}"
            if item.get("page"):
                text += f" / 홈페이지: {item['page']}"
            if item.get("study room time"):
                text += f"\n / 열람실 시간: {item['study room time']}"



            documents.append(text)
    return documents
def process_double_major_data():
    with open("double_major.json", "r", encoding="utf-8") as file:
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

def process_ePortfolio_data():
    with open("smcareer_seoul_25.json", "r", encoding="utf-8") as file:
        ePortfolio_data = json.load(file)

    documents = []

    for item in ePortfolio_data:
        documents.append(
            f"{item['title']} - 링크: {item['url']} / 기간: {item['period']} / 캠퍼스: {item['campus']}"
        )
    return documents

# JSON 데이터 로드 및 벡터화
def load_data_to_chroma():
    collections = {
        "scholarship": (scholarship_collection, process_scholarship_data()),
        "haksa": (haksa_collection, process_haksa_data()),
        "major": (major_collection, process_major_data()),
        "ePortfolio": (ePortfolio_collection, process_ePortfolio_data()),
        "facility": (facility_collection, process_facility_data()),
        "student": (student_collection, process_student_data()),
        "double_major" : (double_major_collection, process_double_major_data()),
        "graduation" : (graduation_collection, process_graduation_data()),
        "service" : (service_collection, process_service_data()),
        "introduction" : (introduction_collection, process_introduction_data()),
        "school" : (school_collection, process_school_data())
    }

    for category, (collection, data) in collections.items():
        if collection.count() == 0:
            print(f"{category} 데이터 저장 중...")
            for idx, text in enumerate(data):
                embedding = embedding_model.encode(text).tolist()
                collection.add(ids=[f"{category}_{idx}"], embeddings=[embedding], metadatas=[{"text": text}])
            print(f"{category} 데이터 저장 완료!")

load_data_to_chroma()

@app.route('/ask', methods=['POST'])
def ask():
    user_question = request.json.get("question")
    print(f"user_question : {user_question}")

    if not user_question:
        return jsonify({"error": "질문을 입력해 주세요."}), 400

    # 사용자 질문 벡터화 후 검색
    user_embedding = embedding_model.encode(user_question).tolist()
    counts = len(user_embedding)

    haksa_results = haksa_collection.query(query_embeddings=[user_embedding], n_results=counts)
    scholarship_results = scholarship_collection.query(query_embeddings=[user_embedding], n_results=counts)
    major_results = major_collection.query(query_embeddings=[user_embedding], n_results=counts)
    ePortfolio_results = ePortfolio_collection.query(query_embeddings=[user_embedding], n_results=counts)
    facility_results = facility_collection.query(query_embeddings=[user_embedding], n_results=counts)
    student_results = student_collection.query(query_embeddings=[user_embedding], n_results=counts)
    double_major_results = double_major_collection.query(query_embeddings=[user_embedding], n_results=counts)
    graduation_results = graduation_collection.query(query_embeddings=[user_embedding], n_results=counts)
    service_results = service_collection.query(query_embeddings=[user_embedding], n_results=counts)
    introduction_results = introduction_collection.query(query_embeddings=[user_embedding], n_results=counts)
    school_results = school_collection.query(query_embeddings=[user_embedding], n_results=counts)

    haksa_docs = [doc["text"] for doc in haksa_results["metadatas"][0] if "text" in doc]
    scholarship_docs = [doc["text"] for doc in scholarship_results["metadatas"][0] if "text" in doc]
    major_docs = [doc["text"] for doc in major_results["metadatas"][0] if "text" in doc]
    ePortfolio_docs = [doc["text"] for doc in ePortfolio_results["metadatas"][0] if "text" in doc]
    facility_docs = [doc["text"] for doc in facility_results["metadatas"][0] if "text" in doc]
    student_docs = [doc["text"] for doc in student_results["metadatas"][0] if "text" in doc]
    double_major_docs = [doc["text"] for doc in double_major_results["metadatas"][0] if "text" in doc]
    graduation_docs = [doc["text"] for doc in graduation_results["metadatas"][0] if "text" in doc]
    service_docs = [doc["text"] for doc in service_results["metadatas"][0] if "text" in doc]
    introduction_docs = [doc["text"] for doc in introduction_results["metadatas"][0] if "text" in doc]
    school_docs = [doc["text"] for doc in school_results["metadatas"][0] if "text" in doc]

    # 검색된 데이터 log
    print(f"검색된 데이터 개수: {len(haksa_results['metadatas'][0])}")

    print(f"검색된 데이터 개수: {len(scholarship_results['metadatas'][0])}")

    print(f"검색된 데이터 개수: {len(major_results['metadatas'][0])}")

    for idx, doc in enumerate(haksa_results["metadatas"][0]):
        print(f"검색 결과 {idx + 1}: {doc['text']}")

    for idx, doc in enumerate(scholarship_results["metadatas"][0]):
        print(f"검색 결과 {idx + 1}: {doc['text']}")

    for idx, doc in enumerate(major_results["metadatas"][0]):
        print(f"검색 결과 {idx + 1}: {doc['text']}")

    for idx, doc in enumerate(facility_results["metadatas"][0]):
        print(f"검색 결과 {idx + 1}: {doc['text']}")

    for idx, doc in enumerate(student_results["metadatas"][0]):
        print(f"검색 결과 {idx + 1}: {doc['text']}")

    for idx, doc in enumerate(double_major_results["metadatas"][0]):
        print(f"검색 결과 {idx + 1}: {doc['text']}")

    for idx, doc in enumerate(graduation_results["metadatas"][0]):
        print(f"검색 결과 {idx + 1}: {doc['text']}")

    for idx, doc in enumerate(service_results["metadatas"][0]):
        print(f"검색 결과 {idx + 1}: {doc['text']}")

    haksa = "\n\n".join(haksa_docs)
    scholarship = "\n\n".join(scholarship_docs)
    major = "\n\n".join(major_docs)
    ePortfolio = "\n\n".join(ePortfolio_docs)
    facility = "\n\n".join(facility_docs)
    student = "\n\n".join(student_docs)
    double_major = "\n\n".join(double_major_docs)
    graduation = "\n\n".join(graduation_docs)
    service = "\n\n".join(service_docs)
    introduction = "\n\n".join(introduction_docs)
    school = "\n\n".join(school_docs)

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": sami_prompt},
            {"role": "system", "content": f"다음은 학사 일정 관련 참고 정보입니다:\n\n{haksa}"},
            {"role": "system", "content": f"다음은 장학금 관련 참고 정보입니다:\n\n{scholarship}"},
            {"role": "system", "content": f"다음은 전공 관련 참고 정보입니다:\n\n{major}"},
            {"role": "system", "content": f"다음은 상명 e-포트폴리오 진로/취업프로그램 정보입니다:\n\n{ePortfolio}"},
            {"role": "system", "content": f"다음은 상명 캠퍼스맵 정보입니다:\n\n{facility}"},
            {"role": "system", "content": f"다음은 학적 관련 정보입니다:\n\n{student}"},
            {"role": "system", "content": f"다음은 전공 제도 관련 정보 입니다:\n\n{double_major}"},
            {"role": "system", "content": f"다음은 졸업 요건 관련 정보 입니다:\n\n{graduation}"},
            {"role": "system", "content": f"다음은 학교 서비스 관련 정보 입니다:\n\n{service}"},
            {"role": "system", "content": f"다음은 사미(SAMI) 챗봇 관련 정보 입니다:\n\n{introduction}"},
            {"role": "system", "content": f"다음은 상명대학교 관련 정보 입니다:\n\n{school}"},
            {"role": "user", "content": user_question}
        ]
    )

    answer = completion.choices[0].message.content
    print(f"answer : {answer}")
    return jsonify({"answer": answer})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False, use_reloader=False)