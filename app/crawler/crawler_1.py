from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urljoin
import pandas as pd
import time
from datetime import datetime
from app.utils.logger import get_logger

# 로거 생성
logger = get_logger(__name__)

def crawler_1_run(config: dict) -> None:

    logger.info("실행 시작")

    # 환경변수 설정
    logger.info("환경변수 설정 시작")
    # url 가져옴
    url = config.get("URL")
    # main에서 validate_crawler_configs를 하지 않을 경우를 대비한 이중 검증
    if not url:
        logger.error("URL 값이 전달되지 않았습니다.")
        raise ValueError("URL 값이 전달되지 않았습니다.")
    logger.info("환경변수 설정 완료")

    # Selenium 설정 및 HTML 요청
    driver = None
    html = None
    try:
        # Selenium 설정
        logger.info("Selenium 설정 시작")
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        logger.info("Selenium 설정 완료")

        logger.info("Selenium driver 실행 시작")
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), 
            options=chrome_options
        )

        # HTML 요청
        logger.info("HTML 요청 시작")
        driver.get(url)

        # JS 로딩 대기하기 위해 WebDriverWait 객체 생성
        wait = WebDriverWait(driver, 10)
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#feedRankingContainer a"))
        )
        html = driver.page_source
    except Exception as e:
        logger.error("HTML 요청 실패:", exc_info=True)
        raise RuntimeError("HTML 요청 실패") from e
    else:
        logger.info("HTML 요청 성공")
    finally:
        if driver:
            driver.quit()
            logger.info("Selenium driver 실행 종료")

    # HTML 파싱
    try:
        logger.info("HTML 파싱 시작")

        # BeautifulSoup 객체로 html 파싱
        soup = BeautifulSoup(html, "html.parser")

        # 필요한 데이터 추출
        news_selector = soup.select("#feedRankingContainer a")

        news_list = []
        for n in news_selector:
            href = n.get("href")
            title_selector = n.select_one("h3.title")
            if href and title_selector:
                title = t if (t:=title_selector.get_text(strip=True)) else "제목 없음"
                news_list.append({
                    "title": title,
                    "href": urljoin(url, href),
                })
    except Exception as e:
        logger.error("HTML 파싱 실패:", exc_info=True)
        raise RuntimeError("HTML 파싱 실패") from e
    else:
        logger.info("HTML 파싱 성공")
        if not news_list:
            logger.warning("HTML 파싱 후 뉴스 항목이 없습니다.")

    # CSV로 저장
    try:
        logger.info("CSV로 저장 시작")
        # csv 파일로 저장
        df = pd.DataFrame(news_list)

        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        timestamp = int(time.time())
        filename = f"news_list_{now}_{timestamp}.csv"

        df.to_csv(filename, index=False, encoding="utf-8-sig")
    except Exception as e:
        logger.error("CSV로 저장 실패:", exc_info=True)
        raise RuntimeError("CSV로 저장 실패") from e
    else:
        logger.info("CSV로 저장 성공")
    
    logger.info("실행 종료")

# 테스트 블록
if __name__ == "__main__":
    from app.config.config import get_crawler_configs, validate_crawler_configs

    logger.info("crawler_1 테스트 시작")

    # 환경 변수 가져옴
    crawler_name = "CRAWLER_1"

    try:
        config = get_crawler_configs(crawler_name)
        validate_crawler_configs(crawler_name)
    except Exception as e:
        logger.error("환경변수 오류", exc_info=True)
        exit()
    
    # 크롤러 실행
    try:
        crawler_1_run(config)
    except Exception as e:
        logger.error("크롤러 오류", exc_info=True)
        exit()
    else:
        logger.info("crawler_1 테스트 완료")