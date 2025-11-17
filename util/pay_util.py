import re

"""
OCR로 추출된 텍스트 리스트에서 '최종 금액'으로 보이는 값 하나 추출
1순위: '합계 / 총액 / total / vat포함 / 결제 / 청구' 주변 숫자
2순위: 전체 숫자 중 가장 큰 값 (fallback)
"""
def extract_final_amount(text_list):
    # 금액 정규식: 1,234 또는 1234 또는 12,345원
    money_pattern = re.compile(r"(?:\d{1,3}(?:,\d{3})+|\d{4,})")

    # 1) 키워드 기반
    keywords = [
        "합계", "총액", "총합", "총금액",
        "total",
        "vat포함", "vat 포함",
        "부가세포함", "부가세 포함",
        "청구금액",
        "총 결제금액",
        "총 계",
        "결제 금액",
        "실제 총 결제 금액"
    ]


    # # 인덱스 순서 그대로 검색
    # for i, text in enumerate(text_list):
    #     low = text.lower()
    #     # 키워드 리스트를 돌면서 k.lower() in low가 하나라도 True 면 바로 뒤에 숫자를 찾으러 다음 for 수행
    #     if any(k.lower() in low for k in keywords):
    #         # 바로 뒤의 숫자를 찾음
    #         for j in range(i, min(i+3, len(text_list))):
    #             if money_pattern.search(text_list[j]):
    #                 return money_pattern.search(text_list[j]).group()

    # 인덱스 순서대로 검색
    for i, text in enumerate(text_list):
        low = text.lower()
        normalized = low.replace(" ", "")

        # 키워드 매칭 (공백 제거 버전 포함)
        if any(k.replace(" ", "").lower() in normalized for k in keywords):

            # 키워드 바로 근처 1~2줄 범위에서 금액 탐색
            for j in range(i, min(i + 3, len(text_list))):
                m = money_pattern.search(str(text_list[j]))
                if m:
                    return m.group()

    # 키워드 없으면 금액 없음
    return None
