import os
from PIL import Image, ImageFont

def get_font(size: int = 10, font_name: str = "NanumGothic.ttf"):
    """
    지정된 크기로 폰트 객체를 반환.
    :param size: 글자 크기 (기본 10)
    :param font_name: font 폴더 내 폰트 파일명
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 상위(프로젝트 루트)
    font_path = os.path.join(base_dir, "font", font_name)

    if not os.path.exists(font_path):
        raise FileNotFoundError(f"폰트 파일이 존재하지 않습니다: {font_path}")

    return ImageFont.truetype(font_path, size)


# 크게 의미 없어서 미사용... ㄴ
def resize_if_small(image: Image.Image):
    """
    작은 이미지는 자동 확대 (세로/가로 중 큰 축 기준 1000px 이하일 경우).
    """
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