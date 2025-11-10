from paddleocr import PaddleOCR
from PIL import Image, ImageDraw, ImageFont
import numpy as np
# 제작
from util.image_util import get_font, resize_if_small   # ← 추가

# import os
# import json
# import pprint

class EduOCR:

    def __init__(self, input_img: str | None = None, lang: str = "korean", **kwargs):
        # ocr 초기화 및 생성 
        self.lang = lang
        self.ocr = PaddleOCR(
            lang=self.lang,
            ocr_version="PP-OCRv5", # 또는 "PP-OCRv3(쓰래기..)", "PP-OCRv4(한글 x)"
            text_det_unclip_ratio=0.5,   # 박스 확장 줄이기
            text_det_box_thresh=0.6,     # 낮은 신뢰도 박스 제거
        )
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
        # OCR 실행
        # 이미지 다이렉트로 넣어야 효과가 좋음 np.array x 
        # ==================================================
        result = self.ocr.ocr(self.in_img)

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
        #TODO 작업 진행해야함 ! 

        return