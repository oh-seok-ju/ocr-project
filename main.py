from main_ocr import EduOCR

def main():
    print("OCR 프로젝트 시작")

    # 입력 이미지 경로 설정 (사용자 환경에 맞게 수정)
    # 테스트 데이터를 구하여 경로를 작성
    img_path = "D:/test_data.PNG"   # 예: "data/test_image.jpg"

    try:
        # EduOCR 객체 생성 및 실행
        ocr = EduOCR(input_img=img_path, lang="korean")
        ocr.simple_ocr()

    except Exception as e:
        print(f"오류 발생: {e}")


if __name__ == "__main__":
    main()
