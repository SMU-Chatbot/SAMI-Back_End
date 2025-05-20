from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
from service import *
from service.chroma import init_collections
from service.data_loader.chroma_loader import load_data_to_chroma, query_chroma_collections

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
embedding_model = load_embedding_model()

# ChromaDB 초기화 (Persistent 모드)
chroma_client = init_chroma()
collections = init_collections(chroma_client)

load_data_to_chroma(embedding_model, collections)

@app.route('/ask', methods=['POST'])
def ask():
    user_question = request.json.get("question")
    print(f"user_question : {user_question}")

    if not user_question:
        return jsonify({"error": "질문을 입력해 주세요."}), 400

    # 사용자 질문 벡터화 후 검색
    user_embedding = embedding_model.encode(user_question).tolist()

    category_texts = query_chroma_collections(user_embedding, collections)

    messages = [{"role": "system", "content": sami_prompt},
            {"role": "system", "content": f"다음은 학사 일정 관련 참고 정보입니다:\n\n{category_texts['haksa_knowledge']}"},
            {"role": "system", "content": f"다음은 장학금 관련 참고 정보입니다:\n\n{category_texts['scholarship_knowledge']}"},
            {"role": "system", "content": f"다음은 전공 관련 참고 정보입니다:\n\n{category_texts['major_knowledge']}"},
            {"role": "system", "content": f"다음은 상명 e-포트폴리오 진로/취업프로그램 정보입니다:\n\n{category_texts['ePortfolio_knowledge']}"},
            {"role": "system", "content": f"다음은 상명 캠퍼스맵 정보입니다:\n\n{category_texts['facility_knowledge']}"},
            {"role": "system", "content": f"다음은 학적 관련 정보입니다:\n\n{category_texts['student_knowledge']}"},
            {"role": "system", "content": f"다음은 전공 제도 관련 정보 입니다:\n\n{category_texts['double_major_knowledge']}"},
            {"role": "system", "content": f"다음은 졸업 요건 관련 정보 입니다:\n\n{category_texts['graduation_knowledge']}"},
            {"role": "system", "content": f"다음은 학교 서비스 관련 정보 입니다:\n\n{category_texts['service_knowledge']}"},
<<<<<<< HEAD
            {"role": "system", "content": f"다음은 사미(SAMI) 챗봇 관련 정보 입니다:\n\n{category_texts['introduction_knowledge']}"},
            {"role": "system", "content": f"다음은 상명대학교 관련 정보 입니다:\n\n{category_texts['school_knowledge']}"},
=======
            {"role": "system", "content": f"다음은 학교 병무 관련 정보 입니다:\n\n{category_texts['military_knowledge']}"},
            {"role": "system", "content": f"다음은 상명대학교 관련 정보 입니다:\n\n{category_texts['school_knowledge']}"},
            {"role": "system", "content": f"다음은 상명대학교 교육과정 관련 정보 입니다:\n\n{category_texts['curriculums_knowledge']}"},
>>>>>>> feature/#12
            {"role": "user", "content": user_question}
    ]

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    answer = completion.choices[0].message.content
    print(f"answer : {answer}")
    return jsonify({"answer": answer})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False, use_reloader=False)