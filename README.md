# project_python-web-crawler-1
A Python web crawler, dockerized and scheduled with cron

<br>

---

<br>

# 프로젝트 개요
- 이 프로젝트는 컨테이너화된 여러 웹 크롤러를 동일한 방식으로 실행 및 관리하기 위한 Python 기반 애플리케이션입니다.
- 공통 실행 진입점을 통해 로컬 환경, Docker, CI/CD 환경에서 동일한 방식으로 크롤러를 실행할 수 있습니다.
- 환경변수 관리, 로깅 기능을 공통 모듈로 분리하여, 새로운 크롤러를 손쉽게 추가할 수 있도록 확장성을 고려해 설계했습니다.

<br>

---

<br>

# 프로젝트 요구사항

## 기능적 요구사항
- 동적 웹 페이지 데이터 수집
    - 환경변수로 URL 관리
    - Selenium + Chrome headless 사용
    - 제목 + 링크 추출
- 데이터 저장
    - CSV 형식
    - 타임스탬프 포함 파일명
    - 환경변수 OUTPUT_DIR 사용해 저장 경로 지정 가능
        - 기본 경로: ./output
- 로깅
    - 환경변수 `LOG_LEVEL`로 로그 레벨 설정 가능
    - 중복 로깅 지양
- 환경변수 관리
    - 필수 값 존재 검증
- 동일 코드로 동일 환경에서 실행 가능
    - 로컬, Docker, CI/CD 모두 적용
- 자동/수동 CI/CD
    - GitHub Actions에서 스케줄 실행
    - 수동 실행 가능
    - 컨테이너 빌드, 실행, output Artifact 업로드 자동화
- 예외 처리
    - 모든 예외 발생 시 로깅 후 애플리케이션 진입점에서 종료코드 반환

## 비기능적 요구사항
- 단일 책임의 원칙 지향
    - 모듈화
    - 차후 확장성 고려
        - 새 크롤러 추가 가능
- 환경 독립성
    - requirements.txt 작성
    - Dockerfile 구성
- 보안
    - 민감 정보는 `.env`(로컬), `GitHub Secret`으로 관리
    - Git과 Docker 관리(`.gitignore`, `.dockerignore`)

<br>

---

<br>

# 프로젝트 구조
```
project_python-web-crawler-1/
│
├─ app/
│  ├─ __init__.py
│  ├─ main.py                  # 애플리케이션 진입점 (컨테이너/로컬 실행)
│  │
│  ├─ crawler/
│  │  ├─ __init__.py
│  │  └─ crawler_1.py          # 크롤링 로직 구현
│  │
│  ├─ config/
│  │  ├─ __init__.py
│  │  └─ config.py             # 환경변수 로드, 검증 함수
│  │
│  └─ utils/
│     ├─ __init__.py
│     └─ logger.py             # LOG_LEVEL 기반 로거 생성 유틸
│
├─ .env                        # 로컬 개발용 환경변수 (Git 제외)
├─ requirements.txt            # Python 패키지 의존성
├─ Dockerfile                  # Docker 이미지 빌드 및 실행 정의
├─ .dockerignore               # Docker 이미지 빌드 시 제외 파일
├─ .gitignore                  # Git 커밋 제외 파일
│
├─ .github/
│  └─ workflows/
│     └─ crawler_1.yml         # GitHub Actions: 자동/수동 크롤러 실행 및 Artifact 업로드
│
└─ README.md                   # 프로젝트 설명 및 트리 구조

```

<br>

## 프로젝트 구조 단위별 상세

### app/main.py
- 애플리케이션 진입점
- 역할
    1. 로거 초기화
    1. 환경변수 로드 및 검증
    1. 크롤러 실행
    1. 예외 발생 시 로깅 후 종료코드 반환

### app/config/config.py
- 환경변수 관리
- 역할
    - `.env` 로드
    - 외부 접근 함수
        - 환경변수 키 검증 후 반환
    - 환경변수 값 검증

### app/crawler/crawler_1.py
- 크롤러 구현
- 역할
    - Selenium + Chrome headless 사용
    - HTML 요청
    - BeautifulSoup으로 HTML 파싱
    - 데이터 추출
    - CSV 저장
        - 환경변수 OUTPUT_DIR 사용 경로 지정 가능
        - 기본 경로: ./output
    - 로깅
        - 실행 단계별 로그 출력

### app/utils/logger.py
- 로그 관리
- 역할
    - 환경변수 LOG_LEVEL 기반 로거 생성
    - 핸들러 중복 검증
    - 로그 출력 포맷 지정

### Dockerfile
- 도커 파일 관리
- 역할
    - Python 3.11 기반 컨테이너 생성
    - ARG로 빌드 시점에 LOG_LEVEL 지정 가능
    - ENV로 빌드 시점의 LOG_LEVEL 적용
    - Chrome + Selenium 실행 환경 구성
    - 의존성 파일 복사 및 설치
    - 소스코드 복사
    - 애플리케이션 진입점을 통해 실행
        - `python -m app.main`

### .dockerignore
- 컨테이너 이미지 빌드시 불필요한 항목 제외

### .gitignore
- Git 커밋에 불필요한 항목 제외

### .github/workflows/crawler_1.yml
- GitHub Actions Workflow
- 역할
    - 스케줄 실행
    - 수동 실행
    - Docker 이미지 빌드
    - GHCR 푸시
    - output 전용 디렉토리 생성
    - Docker 컨테이너 실행
        - Volume 마운트 사용
            - 호스트(runner VM)의 output 디렉토리와 컨테이너 내부 output 디렉토리 연결
    - 호스트의 output/*.csv를 Artifact에 업로드
- 환경 변수
    - GitHub Secret 기반 URL 전달
    - LOG_LEVEL 설정