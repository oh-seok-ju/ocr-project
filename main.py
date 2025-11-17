from main_ocr import EduOCR
import traceback  


def main():
    print("OCR 프로젝트 시작")

    # 입력 이미지 경로 설정 (사용자 환경에 맞게 수정)
    # 테스트 데이터를 구하여 경로를 작성
    # img_path = "D:/test_data.PNG"   # 예: "data/test_image.jpg"

    img_path = "D:/AS 수리완료 내역/250319-0000625_250725 용인 신촌 중학교.pdf"   # 예: "data/test.pdf"
    #"D:\AS 수리완료 내역\250311-0000245_20250311 설봉중(0148)(HA1MQDQJ)-ROM재설치 수리내역서_46200.pdf"
    # 241211-J00004_예솔초 6개.pdf
    # 250318-0000860_250724  김포 나진초등학교.pdf
    # 250319-0000625_250725 용인 신촌 중학교.pdf


    try:
        # EduOCR 객체 생성 및 실행
        ocr = EduOCR(input_img=img_path, lang="korean")
        # simple jpg 테스트
        # ocr.simple_ocr()
        # pdf 테스트
        ocr.pdf_ocr()


    except Exception as e:
        print(f"오류 발생: {e}")
        traceback.print_exc() 


if __name__ == "__main__":
    main()
