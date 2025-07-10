from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
from service import *
from service.chroma import init_collections
from service.data_loader.chroma_loader import load_data_to_chroma, query_chroma_collections
import tiktoken
import time


os.environ["TOKENIZERS_PARALLELISM"] = "false"

# 환경 변수 로드
load_dotenv()
api_key = os.getenv("OPEN_API_KEY")

# Flask 애플리케이션 초기화
app = Flask(__name__)
CORS(app)
client = OpenAI(api_key=api_key)

with open("sami_prompt.txt", "r", encoding="utf-8") as file:
    sami_prompt = file.read()

with open("classify_prompt.txt", "r", encoding="utf-8") as file:
    classify_prompt = file.read()

# Hugging Face 임베딩 모델 로드
embedding_model = load_embedding_model()

# ChromaDB 초기화 (Persistent 모드)
chroma_client = init_chroma()
collections = init_collections(chroma_client)

load_data_to_chroma(embedding_model, collections)

def classify_categories(question, client, categories):
    prompt = classify_prompt.format(
        categories=', '.join(categories),
        question=question
    )

    completion = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages = [
            {"role": "system", "content": prompt}
        ]
    )
    print(completion.choices[0].message.content.strip())
    return completion.choices[0].message.content.strip()

@app.route('/ask', methods=['POST'])
def ask():
    start_time = time.time()

    user_question = request.json.get("question")
    print(f"user_question : {user_question}")

    if not user_question:
        return jsonify({"error": "질문을 입력해 주세요."}), 400

    categories = [
        "haksa_knowledge", "scholarship_knowledge", "major_knowledge", "facility_knowledge",
        "student_knowledge", "double_major_knowledge", "graduation_knowledge", "service_knowledge",
        "introduction_knowledge", "school_knowledge", "military_knowledge", "curriculums_knowledge",
        "professor_knowledge"
    ]

    category = classify_categories(user_question, client, categories)
    print(f"classified category : {category}")

    # 사용자 질문 벡터화 후 검색
    user_embedding = embedding_model.encode(user_question).tolist()

    category_texts = query_chroma_collections(user_embedding, {category: collections[category]})

    messages = [{"role": "system", "content": sami_prompt},
                {"role": "system", "content": f"다음은 {category} 관련 참고 정보입니다:\n\n{category_texts[category]}"},
                {"role": "user", "content": user_question}
    ]

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    answer = completion.choices[0].message.content

    encoding = tiktoken.encoding_for_model("gpt-4o-mini")
    num_tokens = len(encoding.encode(answer))
    print(f"num_tokens : {num_tokens}")

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"elapsed_time : 응답 속도: {elapsed_time}")

    print(f"answer : {answer}")
    return jsonify({"answer": answer})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False, use_reloader=False)