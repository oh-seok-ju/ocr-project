import streamlit as st
import tempfile
from main_ocr import EduOCR

def main():
    st.title("[OCR] 교육청 명세서 OCR")
    st.caption("[OCR] PDF 명세서에서 페이지별 최종 금액 후보를 추출합니다.")

    lang = "korean"
    uploaded_file = st.file_uploader("PDF 파일 업로드", type=["pdf"])

    # 세션 초기화
    if "page_summaries" not in st.session_state:
        st.session_state.page_summaries = None
    if "page_images" not in st.session_state:
        st.session_state.page_images = None
    if "uploaded_filename" not in st.session_state:
        st.session_state.uploaded_filename = None

    if uploaded_file is not None:
        st.info(f"업로드된 파일: `{uploaded_file.name}`")

        # 파일이 바뀌면 이전 OCR 결과 초기화
        if st.session_state.uploaded_filename != uploaded_file.name:
            st.session_state.page_summaries = None
            st.session_state.page_images = None
            st.session_state.uploaded_filename = uploaded_file.name

        # 임시 파일 저장
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name

        # 버튼: OCR 실제 실행은 여기서 딱 한 번
        if st.button("OCR 실행"):
            with st.spinner("OCR 처리 중..."):
                ocr = EduOCR(input_img=tmp_path, lang=lang)
                page_summaries, page_images = ocr.pdf_ocr()

            st.session_state.page_summaries = page_summaries
            st.session_state.page_images = page_images

    # 버튼 블록 밖에서, 세션에 값이 있으면 항상 그리기
    if st.session_state.page_summaries is not None:
        page_summaries = st.session_state.page_summaries
        page_images = st.session_state.page_images

        st.success("OCR 완료!")
        st.subheader("페이지별 금액 요약")

        final_choices = []

        for summary, page_img in zip(page_summaries, page_images):
            page_no = summary["page"]
            amount = summary["amount"]

            st.markdown(f"### 📄 페이지 {page_no}")
            st.image(page_img, caption=f"페이지 {page_no} OCR 결과", use_container_width=True)

            final_amount = None

            if amount is None:
                st.warning("추출된 최종 금액 없음 혹은 키워드 미검출 또는 숫자 인식 실패")
                manual_amount = st.text_input(
                    f"[p{page_no}] 직접 금액을 입력하세요 (예: 470,800 또는 470800)",
                    key=f"manual_{page_no}",
                )
                if manual_amount.strip():
                    final_amount = manual_amount.strip()
            else:
                st.metric(label="추출된 최종 금액 (자동)", value=str(amount))
                confirm = st.radio(
                    f"[p{page_no}] 이 금액이 맞나요?",
                    ("예", "아니요"),
                    horizontal=True,
                    key=f"confirm_{page_no}",
                )

                if confirm == "예":
                    final_amount = amount
                else:
                    manual_amount = st.text_input(
                        f"[p{page_no}] 정확한 금액을 직접 입력하세요",
                        value="",
                        key=f"manual_{page_no}",
                    )
                    if manual_amount.strip():
                        final_amount = manual_amount.strip()

            # with st.expander(f"[p{page_no}] 이 페이지 인식 텍스트 전체 보기"):
            #     st.write("\n".join(summary["texts"]))

            final_choices.append(
                {
                    "page": page_no,
                    "auto_amount": amount,
                    "final_amount": final_amount,
                }
            )

        st.subheader("최종 선택된 금액 요약")
        st.table(final_choices)

if __name__ == "__main__":
    main()
