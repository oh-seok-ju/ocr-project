from paddleocr import PaddleOCR, PPStructureV3
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from pathlib import Path

# 제작
from util.image_util import get_font, resize_if_small
from util.pay_util import extract_final_amount

# import os
# import json
# import pprint

class EduOCR:

    def __init__(self, input_img: str | None = None, lang: str = "korean", **kwargs):
        # 초기 값(언어)
        self.lang = lang
        # 파일 in/out
        self.in_img = input_img
        self.out_img = None
        # 최종 결과 result 
        self.ocr_result = {}

    """
    *** 함수1 : 기본 OCR 
    기본 jpg 이미지를 활용한 OCR 코드 테스트용 & 간단 이미지용 입니다. 
    이미지 저장 기능 및 이미지 로드시 util 함수의 이미지 사이즈 수정 비활성화
    """
    def simple_ocr(self):
        if self.in_img is None:
            raise ValueError("입력 이미지 경로가 설정되지 않았습니다.")
        # ==================================================
        # OCR 초기화 및 실행
        # 이미지 다이렉트로 넣어야 효과가 좋음 np.array x 
        # ==================================================
        ocr_image = PaddleOCR(
            lang=self.lang,
            ocr_version="PP-OCRv5", # 또는 "PP-OCRv3(쓰래기..)", "PP-OCRv4(한글 x)"
            text_det_unclip_ratio=0.5,   # 박스 확장 줄이기
            text_det_box_thresh=0.6,     # 낮은 신뢰도 박스 제거
        )

        result = ocr_image.ocr(self.in_img)

        # 결과가 없으면 리턴.. 
        if not result or not isinstance(result[0], dict):
            print("결과 구조가 비어 있거나 인식되지 않았습니다.")
            return

        """
            rec_boxes: 단순 사각형 [x_min, y_min, x_max, y_max]
            rec_polys: 네 꼭짓점 좌표 [[x1,y1],[x2,y2],[x3,y3],[x4,y4]]
            택 1 해당 선택에 따른 코드 수정 필요
        """
        res = result[0]  # 첫 번째 페이지 결과
        # boxes = res.get("rec_polys", [])
        boxes = res.get("rec_boxes", [])
        texts = res.get("rec_texts", [])
        scores = res.get("rec_scores", [])

        # 그림 그리기 .convert("RGB")
        image = Image.open(self.in_img).convert("RGB")
        draw = ImageDraw.Draw(image)

        # 박스 & 텍스트 시각화
        for box, text, score in zip(boxes, texts, scores):

            box = np.array(box).astype(int)

            """
            앞서 설정에서 boxes변수에 따라 분기 발생
            rec_boxes: if 문
            rec_polys: else 문
            """
            if box.ndim == 1 and len(box) == 4:
                x_min, y_min, x_max, y_max = box
            # else:
            #     print("else 시작")
            #     # rec_polys 형태일 경우 안전 처리
            #     x_min, y_min = box[:, 0].min(), box[:, 1].min()
            #     x_max, y_max = box[:, 0].max(), box[:, 1].max()

            # 박스 생성
            draw.rectangle([(x_min, y_min), (x_max, y_max)], outline=(0, 255, 0), width=1)

            # 텍스트 출력
            draw.text( (x_min, max(y_min - 10, 0)), f"{text}", font=get_font(10), fill=(255, 0, 0))

            # 터미널에서 스코어 확인 확인
            print(f"Detected: {text} 정확도 {score:.2f})")

        # 미리보기 (시각화 이미지 바로 열기)
        image.show()

        # # 결과 저장 (비활성화) - 추후 필요시 사용...
        # base, ext = os.path.splitext(self.in_img)
        # self.out_img = f"{base}_ocr_result{ext}"
        # image.save(self.out_img)
        # print(f"OCR 결과 이미지 저장 완료: {self.out_img}")
    
    
    """
    *** 함수2 : 교육청에 맞는 PDF to OCR 진행 
    문제1. 단일/다중 페이지를 모두 OCR 필요 .. 필요시 화면에서 1장단위로 입력할 수 있게 조정 필요..
    문제2. 해당 OCR후 총 금액 관련된 정보만 출력
    """

    def pdf_ocr(self):
        if not self.in_img or Path(self.in_img).suffix.lower() != ".pdf":
            raise ValueError("유효한 PDF(.pdf) 경로가 설정되지 않았습니다.")
        
        """
        추가 기능
        # use_doc_orientation_classify= True/False  
        # 문서가 90도/180도 회전돼 있는지 자동 판단하는 기능

        # use_doc_unwarping= True/False 
        # → 스캔본이 휘었거나 구겨졌을 때 펼치는 보정 기능

        # use_textline_orientation= True/False  
        # → 텍스트 라인이 기울었는지 판단하는 기능 끔
        """
        ocr_image = PaddleOCR(
            lang=self.lang,
            ocr_version="PP-OCRv5", # 또는 "PP-OCRv3(쓰래기..)", "PP-OCRv4(한글 x)"
            text_det_box_thresh=0.6,     # 낮은 신뢰도 박스 제거
            use_doc_orientation_classify=False,  # 문서 기울기(orientation) 자동 판단 모델 OFF
            use_doc_unwarping=False,            # 문서 펼침/왜곡 보정(unwarping) 모델 OFF
            use_textline_orientation=False,      # 텍스트 라인 방향 판단 모델 OFF
        )

        from pdf2image import convert_from_path

        # === 여기부터 PDF -> 이미지 변환 ===
        POPPLER_PATH = r"D:\poppler-25.07.0\Library\bin"  # ← 실제 poppler 설치 경로로 변경
        # dpi=150,
        pages = convert_from_path(self.in_img, poppler_path=POPPLER_PATH)

        all_results = []
        page_summaries = []   # 페이지별 텍스트/금액 요약 저장용

        for page_idx, page in enumerate(pages, start=1):
            print(f"\n=== {page_idx} 페이지 OCR 시작 ===")

            # PIL.Image → ndarray
            img_np = np.array(page)

            # 2) PaddleOCR 수행
            result = ocr_image.ocr(img_np)

            if not result:
                print("결과가 비어 있습니다.")
                page_summaries.append({
                    "page": page_idx,
                    "amount": None,
                    "texts": [],
                })
                continue

            # simple_ocr와 동일한 dict 구조일 경우
            res = result[0]
            boxes = res.get("rec_boxes", [])
            texts = res.get("rec_texts", [])
            scores = res.get("rec_scores", [])

            page_draw = page.convert("RGB")
            draw = ImageDraw.Draw(page_draw)

            #추출된 텍스트 모음
            page_texts = []

            for box, text, score in zip(boxes, texts, scores):
                box = np.array(box).astype(int)

                #  x_min, y_min 좌상단
                #  x_max, y_max 우하단
                if box.ndim == 1 and len(box) == 4:
                    x_min, y_min, x_max, y_max = box
                # else:
                #     x_min, y_min = box[:, 0].min(), box[:, 1].min()
                #     x_max, y_max = box[:, 0].max(), box[:, 1].max()

                draw.rectangle([(x_min, y_min), (x_max , y_max)], outline=(0, 255, 0), width=2)
                draw.text((x_min, max(y_min - 20, 0)), f"{text}", font=get_font(15), fill=(255, 0, 0))

                print(f"[page : {page_idx}] {text} 정확도 {score:.2f})")

                # page text 추가
                page_texts.append(text)

                # json 형식으로 api에서 쓸 수 있게 생각 해봄
                all_results.append({
                    "page": page_idx,
                #     "bbox": [int(x_min), int(y_min), int(x_max), int(y_max)],
                    "text": text,
                    "score": float(score),
                })


            # 현재 페이지에서의 후보 금액 추출
            page_amount = extract_final_amount(page_texts) if page_texts else None

            page_summaries.append({
                "page": page_idx,
                "amount": page_amount,
                "texts": page_texts,
            })

            # 그리기 나중에 필요하면 저장도 생각
            page_draw.show()


        # 페이지별 요약 출력
        print("\n=== 페이지별 금액 요약 ===")
        for summary in page_summaries:
            print(f"- p{summary['page']}: {summary['amount']}")

        # # 클래스 내부에 결과 저장
        # self.ocr_result = {
        #     "pages": page_summaries,
        #     "all_results": all_results,
        # }

        # 여기서는 '전체 최종 금액'은 자동으로 하나만 고르지 않고,
        # 호출하는 쪽에서 page_summaries를 보고 선택하게 하는 흐름으로 둠.
        # return page_summaries
