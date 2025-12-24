import os
from dotenv import load_dotenv

# .env 로드
load_dotenv()

# class 기반의 리팩토링을 전제로 딕셔너리 형태로 코딩
_CRAWLER_CONFIGS = {
    "CRAWLER_1": {
        "URL": os.getenv("CRAWLER_1_URL")
    }
}

# 외부에서 접근하는 함수
def get_crawler_configs(crawler_name: str) -> dict:
    
    if crawler_name not in _CRAWLER_CONFIGS:
        raise KeyError(f"{crawler_name}: CONFIG 키가 정의되지 않았습니다.")
    
    return _CRAWLER_CONFIGS[crawler_name]

# 필수 환경변수 값 존재 검증 함수
def validate_crawler_configs(crawler_name: str) -> None:

    cfg = get_crawler_configs(crawler_name)

    if not cfg.get("URL"):
        raise ValueError(f"{crawler_name}: 정의된 CONFIG 내부의 URL 값이 존재하지 않습니다.")