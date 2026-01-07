from app.config.config import get_crawler_configs, validate_crawler_configs
from app.utils.logger import get_logger
from app.crawler.crawler_1 import crawler_1_run

def main() -> None:
    """
    애플리케이션의 진입점
    - 메인 로거
    - 환경변수 로드
    - 환경변수 검증
    - 크롤러 실행
    - 예외 발생시 로깅 및 raise
    """

    logger = get_logger(__name__)
    logger.info("애플리케이션 실행 시작")

    crawler_name = "CRAWLER_1"

    # 환경변수 로드 및 검증
    try:
        logger.info("환경변수 로드 및 검증 시작")
        config = get_crawler_configs(crawler_name) # 환경변수 키 로드 및 검증
        validate_crawler_configs(crawler_name) # 환경변수 값 검증
    except Exception:
        logger.error("환경변수 로드 및 검증 오류", exc_info=True)
        raise # 예외를 진입점으로 전파
    else:
        logger.info("환경변수 로드 및 검증 성공")
    
    # 크롤러 실행
    try:
        logger.info(f"{crawler_name} 실행 시작")
        crawler_1_run(config)
    except Exception:
        logger.error(f"{crawler_name} 실행 오류", exc_info=True)
        raise # 예외를 진입점으로 전파
    else:
        logger.info(f"{crawler_name} 실행 성공")
    
    logger.info("애플리케이션 실행 종료")

if __name__=="__main__":
    import sys

    try:
        main()
    except Exception:
        sys.exit(1)
    else:
        sys.exit(0)