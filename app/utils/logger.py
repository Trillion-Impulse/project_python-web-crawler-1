import logging
import os

# logger 생성 함수
def get_logger(name: str) -> logging.Logger:

    # 환경변수에서 로그 레벨 가져오기, 없으면 INFO
    log_level_str = os.getenv("LOG_LEVEL", "INFO").upper()
    log_level = getattr(logging, log_level_str, logging.INFO)

    # 로거 생성
    logger = logging.getLogger(name)
    logger.setLevel(log_level)  # 최소 출력 레벨 설정

    # 중복 핸들러 추가 방지
    if not logger.handlers:
        # 콘솔 출력 핸들러
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)  # 핸들러 자체의 최소 출력 레벨도 설정 가능 / 로그 레벨 이중 제한 가능

        # 로그 출력 포맷 지정
        formatter = logging.Formatter(
            "[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        console_handler.setFormatter(formatter)

        # 핸들러 로거에 등록
        logger.addHandler(console_handler)
        logger.propagate = False

    return logger