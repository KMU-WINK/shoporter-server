from selenium import webdriver
from account_information import id, password
import time


driver = webdriver.Chrome('./chromedriver')
driver.implicitly_wait(3)

driver.get("https://sell.smartstore.naver.com/#/login")
script_injection = "setTimeout(function(){var inp = document.querySelectorAll('input');if(inp.length>0){var ev = new Event('input');inp[0].value ='" + id+"';inp[0].dispatchEvent(ev);inp[1].value ='"+ password +"';inp[1].dispatchEvent(ev);document.querySelector('#loginButton').click();}},500);"

driver.execute_script(script_injection)
time.sleep(1)

driver.get('https://sell.smartstore.naver.com/o/v3/iframe/n/sale/delivery')
time.sleep(1)

# 조회기간 오늘 버튼 클릭
driver.find_element_by_xpath('//*[@id="__app_root__"]/div/div[2]/div[2]/div[1]/table/tbody/tr[1]/td/div[1]/div[2]/div/ul/li[1]/button').click()
time.sleep(1)
# 검색 버튼 클릭
driver.find_element_by_xpath('//*[@id="__app_root__"]/div/div[2]/div[2]/div[2]/button').click()
time.sleep(1)

# 하단 목록의 금일 결제 총 개수 데이터 저장 후 출력
payment = driver.find_element_by_xpath('//*[@id="__app_root__"]/div/div[2]/div[3]/div[1]/h3/b')
print(payment.text)

driver.close()