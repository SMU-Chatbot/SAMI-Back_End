import json

def process_facility_data():
    with open("Training_Data/facility.json", "r", encoding="utf-8") as file:
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