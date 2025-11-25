# app.py = 예전버전 사용 x

import streamlit as st
import tempfile
from main_ocr import EduOCR

def main():
    st.title("(OCR)교육청 명세서 POC")
    st.caption("명세서에서 페이지별 최종 금액 후보를 추출합니다.")

    # 언어 선택 (나중 확장 대비)
    lang = st.selectbox("OCR 언어", ["korean", "en"], index=0)

    uploaded_file = st.file_uploader("PDF 파일 업로드", type=["pdf"])

    if uploaded_file is not None:
        st.info(f"업로드된 파일: `{uploaded_file.name}`")

        # 임시 파일로 저장 (PaddleOCR + pdf2image는 경로 기반이라)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name

        if st.button("OCR 실행"):
            with st.spinner("OCR 처리 중..."):
                ocr = EduOCR(input_img=tmp_path, lang=lang)
                page_summaries, page_images = ocr.pdf_ocr(show_debug_window=False)

            st.success("OCR 완료!")

            st.subheader("페이지별 금액 요약")

            for summary, page_img in zip(page_summaries, page_images):
                page_no = summary["page"]
                amount = summary["amount"]

                st.markdown(f"### 📄 페이지 {page_no}")

                # 페이지 이미지 + 박스 표시
                st.image(page_img, caption=f"페이지 {page_no} OCR 결과", use_container_width=True)

                # 금액 정보
                if amount is None:
                    st.warning("추출된 최종 금액 없음 (키워드 미검출 또는 숫자 인식 실패)")
                else:
                    st.metric(label="추출된 최종 금액", value=str(amount))

                # 세부 텍스트는 접을 수 있게
                with st.expander("이 페이지 인식 텍스트 전체 보기"):
                    st.write("\n".join(summary["texts"]))

if __name__ == "__main__":
    main()
