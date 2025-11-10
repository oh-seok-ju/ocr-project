from paddleocr import PaddleOCR
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os
import json
import pprint

class EduOCR:

    def __init__(self, input_img: str | None = None, lang: str = "korean", **kwargs):
        # ocr 초기화 및 생성 
        self.lang = lang
        self.ocr = PaddleOCR(lang=self.lang)
        # 파일 in/out
        self.in_img = input_img
        self.out_img = None
        # 최종 결과 result 
        self.ocr_result = {}



    # 이미지 크기 자동 조정 함수
    def resize_if_small(self, image: Image.Image):
        """작은 이미지는 자동 확대 (세로/가로 중 큰 축 기준 1000px 이하일 경우)."""
        w, h = image.size
        scale = 1.0

        if max(w, h) < 700:
            scale = 2.0
        elif max(w, h) < 1000:
            scale = 1.5

        if scale > 1.0:
            new_size = (int(w * scale), int(h * scale))
            image = image.resize(new_size, Image.LANCZOS)
            print(f"이미지 자동 확대: {w}x{h} → {new_size}")

        return image


    def simple_ocr(self):
        if self.in_img is None:
            raise ValueError("입력 이미지 경로가 설정되지 않았습니다.")

        # ocr 전달 및 결과 저장
        result = self.ocr.ocr(self.in_img)

        if not result or not isinstance(result[0], dict):
            print("⚠️ 결과 구조가 비어 있거나 인식되지 않았습니다.")
            return

        res = result[0]  # 첫 번째 페이지 결과
 
        """
            rec_boxes: 단순 사각형 [x_min, y_min, x_max, y_max]
            rec_polys: 네 꼭짓점 좌표 [[x1,y1],[x2,y2],[x3,y3],[x4,y4]]
            택 1 해당 선택에 따른 코드 수정 필요
        """
        # boxes = res.get("rec_boxes", []) or res.get("rec_polys", [])
        boxes = res.get("rec_boxes", [])
        texts = res.get("rec_texts", [])
        scores = res.get("rec_scores", [])

        # 원본 이미지 로드 .convert("RGB")
        image = Image.open(self.in_img)
        draw = ImageDraw.Draw(image)


        # 폰트 설정 (이미지에 글자 넣을때 사용)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        img_w, img_h = image.size
        font_size = max(12, int(min(img_w, img_h) * 0.02))  # 전체 크기의 약 2%
        font_path = os.path.join(base_dir, "font", "NanumGothic.ttf")
        font = ImageFont.truetype(font_path, font_size)


        # 박스 & 텍스트 시각화
        for box, text, score in zip(boxes, texts, scores):

            ### simple as-is ####
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

            # 박스 및 텍스트 출력
            draw.rectangle([(x_min, y_min), (x_max, y_max)], outline=(0, 255, 0), width=1)
            # 이미지에 텍스트 까지 그리기 v1 / v2
            # draw.text((x_min, max(y_min - 15, 0)), f"{text} ({score:.2f})", font=font, fill=(255, 0, 0))
            # draw.text(top_left, f"{text} ({score:.2f})", font=font, fill=(255, 0, 0))
            
            # 터미널에서 스코어 확인 확인
            print(f"Detected: {text} 정확도 {score:.2f})")

        # ✅ 미리보기 (시각화 이미지 바로 열기)
        image.show()

        # # 결과 저장 비활성화
        # base, ext = os.path.splitext(self.in_img)
        # self.out_img = f"{base}_ocr_result{ext}"
        # image.save(self.out_img)
        # print(f"OCR 결과 이미지 저장 완료: {self.out_img}")