from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium.webdriver.common.keys import Keys

import csv
import pandas as pd
import re

# URL 파일 불러오기
df = pd.read_csv("C:/Users/USER/Desktop/airbnb_review_urls.csv")
df.head()

# Emoji package
!pip install emoji
from emoji import core

def cleaned_text(text):
    # 이모지 및 특수 문자 제거 (한글, 영문, 숫자만 남김)
    text = text.replace("\xa0", " ")  # 특수 공백을 일반 공백으로 변환
    text = re.sub(r"[^가-힣a-zA-Z0-9\s]", "", text)  # 한글, 영어, 숫자, 공백만 남기기
    return text

# WebDriver 실행
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# 총 데이터 개수
total_num = 0

# for문 이용해서 리뷰 페이지 열기
for i in range(750, 1000):
    url = df.loc[i, 'url']
    driver.get(url)

    time.sleep(5) # 페이지 로딩 대기

    # 페이지가 완전히 로드될 때까지 대기
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    print("페이지 로드 완료")

    # 페이지 소스 가져와서 파싱
    soup = BeautifulSoup(driver.page_source, "lxml")

    # 리뷰 포함된 div 찾기 (답글 제외)
    review_divs = soup.find_all('div', {'class': 'r1bctolv atm_c8_1sjzizj atm_g3_1dgusqm atm_26_lfmit2_13uojos atm_5j_1y44olf_13uojos atm_l8_1s2714j_13uojos dir dir-ltr'})

    # 엑셀 파일에 review 추가하기
    with open("C:/Users/USER/Desktop/review output.csv", 'a', newline='') as f:
        writer = csv.writer(f)

        # 중복 제거
        num_reviews = len(review_divs)

        if num_reviews >= 12:
            review_divs = review_divs[6:]
            num_reviews -= 6

        else:
            review_divs = review_divs[num_reviews // 2:]
            num_reviews //= 2

        print(num_reviews)
        total_num += num_reviews
            
        # 엑셀 파일에 데이터 추가   
        for div in review_divs:
            spans = div.find_all('span', class_='l1h825yc atm_kd_19r6f69_24z95b atm_kd_19r6f69_1xbvphn_1oszvuo dir dir-ltr')
            for span in spans:
                review_text = span.text.strip()
                # emoji 제거
                clean_text = core.replace_emoji(review_text, replace="")
                # 특수문자 제거
                clean_review = cleaned_text(clean_text)
                if clean_review:  # 빈 문자열 방지
                    print("추출된 리뷰:", clean_review)
                    writer.writerow([clean_review])

    time.sleep(2)
    print("완료", i+1)

print("데이터 총 개수 :", total_num)