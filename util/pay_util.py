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

    candidates = []  # 금액을 모을 리스트

    # 인덱스 순서대로 검색
    for i, text in enumerate(text_list):
        low = text.lower()
        normalized = low.replace(" ", "")

        # 키워드 매칭 (공백 제거 버전 포함)
        if any(k.replace(" ", "").lower() in normalized for k in keywords):

            # 이 키워드 주변 1~2줄 범위에서 금액 탐색
            for j in range(i, min(i + 3, len(text_list))):
                line = str(text_list[j])
                for m in money_pattern.finditer(line):
                    try:
                        value = int(m.group().replace(",", ""))
                    except ValueError:
                        continue
                    candidates.append(value)

    # 키워드 자체가 하나도 없거나, 주변에서 금액을 못 찾았으면 없음
    if not candidates:
        return None

    # 후보들 중 가장 큰 금액을 최종값으로
    return f"{max(candidates):,d}"
