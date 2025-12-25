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


def crawler_1_run(config: dict) -> None:
    # 환경변수 설정
    print("환경변수 설정 시작")
    # url 가져옴
    url = config.get("URL")
    # main에서 validate_crawler_configs를 하지 않을 경우를 대비한 이중 검증
    if not url:
        raise ValueError(f"URL 값이 전달되지 않았습니다.")

    # Selenium 설정 및 HTML 요청
    driver = None
    html = None
    try:
        # Selenium 설정
        print("Selenium 설정 시작")
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), 
            options=chrome_options
        )
        print("Selenium 설정 완료")

        # HTML 요청
        print("HTML 요청 시작")
        driver.get(url)

        # JS 로딩 대기하기 위해 WebDriverWait 객체 생성
        wait = WebDriverWait(driver, 10)
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#feedRankingContainer a"))
        )
        html = driver.page_source
    except Exception as e:
        print("HTML 요청 실패:", e)
        raise RuntimeError("HTML 요청 실패") from e
    else:
        print("HTML 요청 성공")
    finally:
        if driver:
            driver.quit()

    # HTML 파싱
    try:
        print("HTML 파싱 시작")

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
        print("HTML 파싱 실패:", e)
        raise RuntimeError("HTML 파싱 실패") from e
    else:
        print("HTML 파싱 성공")

    # CSV로 저장
    try:
        print("CSV로 저장 시작")
        # csv 파일로 저장
        df = pd.DataFrame(news_list)

        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        timestamp = int(time.time())
        filename = f"news_list_{now}_{timestamp}.csv"

        df.to_csv(filename, index=False, encoding="utf-8-sig")
    except Exception as e:
        print("CSV로 저장 실패:", e)
        raise RuntimeError("CSV로 저장 실패") from e

# 테스트 블록
if __name__ == "__main__":
    from app.config.config import get_crawler_configs, validate_crawler_configs

    # 환경 변수 가져옴
    crawler_name = "CRAWLER_1"

    try:
        config = get_crawler_configs(crawler_name)
        validate_crawler_configs(crawler_name)
    except Exception as e:
        print("환경변수 오류", e)
        exit()
    
    # 크롤러 실행
    try:
        crawler_1_run(config)
    except Exception as e:
        print("크롤러 오류", e)
        exit()
    else:
        print("crawler_1 실행 완료")