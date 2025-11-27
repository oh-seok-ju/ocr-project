# OCR 프로젝트 - 교육청 적용 POC


## PaddleOCR 활용 
https://github.com/PaddlePaddle/PaddleOCR/blob/main/readme/README_ko.md

```bash
# // 필수 라이브러리 uv설치시 uv add ~
pip install paddlepaddle
pip install paddleocr

# **gpu**
pip install paddlepaddle-gpu

```

## 📁프로젝트 구조
```
ocr-project/
├─ .venv/                 # 가상환경 (OS별로 별도 생성)
├─ main_ocr.py            # OCR 코드 스크립트
├─ main.py                # *실행 스크립트
├─ pyproject.toml         # uv 설정 파일
├─ uv.lock                # 패키지 버전 고정
├─ README.md              # 이 파일
└─ ... (기타 코드)
```

## ⚙️사전 준비
| 항목                 | 내용                                           |
| ------------------ | -------------------------------------------- |
| Python 버전          | 3.11 이상                                      |
| 필수 도구              | [uv](https://github.com/astral-sh/uv) 또는 pip |


## 🪟VM(가상 환경 설정)

### 가상환경 생성(window)
```powershell
cd C:\Users\<사용자>\Desktop\OCR\ocr-project
uv venv .venv
```

**가상환경 활성화**
```powershell
& .\.venv\Scripts\Activate.ps1
```

**패키지 설치**
```powershell
uv sync
```
---

### 가상환경 생성(linux/macOS)
```bash
# // 윈도우에서 가져온 .venv는 삭제
cd ~/Desktop/OCR/ocr-project
rm -rf .venv
```

**가상환경 생성**
```bash
uv venv .venv
```

**가상환경 활성화**
```bash
source .venv/bin/activate
```

**패키지 설치**
```bash
uv sync
```
---

### 기타 가상환경 체크
**설정 잡기(vscode)**
Interpreter 변경 필요 (ctrl + shift + p) 아래 환경체크를 통해 나온 경로 설정하기 

**환경 체크**
**window**
```powershell
(Get-Command python).Source
```

**macOS/linux**
```bash
which python   /   python3
```

**라이브러리 체크**
```bash
uv pip list 
```
--- 

## 우분투 서버에서 실행할때 가상환경 접속 및 streamlit 서버 실행(현 서버) tmux 사용

```bash

tmux new -s <세션 이름> // 세션 분리 생성 

tmux ls // 기존 세션 확인

tmux attach -t <세션 이름>  // 기존 세션 접근

tmux kill-session -t <세션 이름> // 세션 종료

Ctrl + B → 𝄽 → D  // tumx 세션에서 빠져 나오기 

# 세션 내부에서 streamlit 서버 기동
streamlit run app2.py --server.address 0.0.0.0 --server.port <포트번호>

```

## 기타
** pdf2image 관련**
 https://m.blog.naver.com/chandong83/222262274082