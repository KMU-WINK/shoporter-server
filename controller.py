import traceback
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from account_information import id, password
import time

from flask import request, url_for, jsonify
from flask_api import FlaskAPI, status, exceptions

app = FlaskAPI(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/smart-store/today-payment', methods=['GET'])
def today_payment():
    options = Options()
    options.add_argument("--disable-gpu")  # 그래픽 가속을 사용할 때 크롬에서 버그를 일으키는 현상이 있음
    options.add_argument("--no-sandbox")  # 앗 이런 오류! 방지
    options.add_argument("enable-automation")  # 알림 표시줄 제거
    options.add_argument("--disable-infobars")  # 인포 박스 제거
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome('./chromedriver', options=options)
    driver.implicitly_wait(2)

    driver.get("https://sell.smartstore.naver.com/#/login")
    script_injection = "setTimeout(function(){var inp = document.querySelectorAll('input');if(inp.length>0){var ev = new Event('input');inp[0].value ='" + id + "';inp[0].dispatchEvent(ev);inp[1].value ='" + password + "';inp[1].dispatchEvent(ev);document.querySelector('#loginButton').click();}},500);"

    driver.execute_script(script_injection)
    time.sleep(1)

    driver.get('https://sell.smartstore.naver.com/o/v3/iframe/n/sale/delivery')
    time.sleep(1)

    # 조회기간 오늘 버튼 클릭
    driver.find_element_by_xpath(
        '//*[@id="__app_root__"]/div/div[2]/div[2]/div[1]/table/tbody/tr[1]/td/div[1]/div[2]/div/ul/li[1]/button').click()
    time.sleep(1)
    # 검색 버튼 클릭
    driver.find_element_by_xpath('//*[@id="__app_root__"]/div/div[2]/div[2]/div[2]/button').click()

    # 하단 목록의 금일 결제 총 개수 데이터 저장 후 출력
    payment = driver.find_element_by_xpath('//*[@id="__app_root__"]/div/div[2]/div[3]/div[1]/h3/b').text
    driver.quit()

    return jsonify({'today_payment': payment}), status.HTTP_200_OK

@app.route('/smart-store/product-list', methods=['GET'])
def product_list():
    options = Options()
    options.add_argument("--disable-gpu")  # 그래픽 가속을 사용할 때 크롬에서 버그를 일으키는 현상이 있음
    options.add_argument("--no-sandbox")  # 앗 이런 오류! 방지
    options.add_argument("enable-automation")  # 알림 표시줄 제거
    options.add_argument("--disable-infobars")  # 인포 박스 제거
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome('./chromedriver', options=options)
    driver.implicitly_wait(2)

    # 상품조회 /수정 페이지 에서 상품목록 가져오기
    driver.get("https://sell.smartstore.naver.com/#/login")
    script_injection = "setTimeout(function(){var inp = document.querySelectorAll('input');if(inp.length>0){var ev = new Event('input');inp[0].value ='" + id + "';inp[0].dispatchEvent(ev);inp[1].value ='" + password + "';inp[1].dispatchEvent(ev);document.querySelector('#loginButton').click();}},500);"
    driver.execute_script(script_injection)
    time.sleep(1)

    driver.get("https://sell.smartstore.naver.com/#/products/origin-list")
    time.sleep(3)

    # 상품명 가져오기
    product_title = driver.find_element_by_xpath(
        '//*[@id="seller-content"]/ui-view/div/ui-view[2]/div[1]/div[2]/div[3]/div/div/div/div/div[3]/div[2]/div/div/div/div[2]').text
    driver.quit()
    return jsonify({'product_list': product_title}), status.HTTP_200_OK #추후 상품 이름과 가격을 리스트로 던져주는 기능 개발 이번엔 아직 안 씀

