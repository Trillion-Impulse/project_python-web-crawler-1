# project_python-web-crawler-1
A Python web crawler, dockerized and scheduled with cron

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