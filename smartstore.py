from selenium import webdriver
from account_information import id, password


driver = webdriver.Chrome('/chromedriver')
driver.implicitly_wait(3)

driver.get("https://sell.smartstore.naver.com/#/login")
script_injection = "setTimeout(function(){var inp = document.querySelectorAll('input');if(inp.length>0){var ev = new Event('input');inp[0].value ='" + id+"';inp[0].dispatchEvent(ev);inp[1].value ='"+ password +"';inp[1].dispatchEvent(ev);document.querySelector('#loginButton').click();}},500);";

driver.execute_script(script_injection)

# 심사 안내 팝업 종료
driver.find_element_by_xpath('/html/body/div[1]/div/div/div[3]/div[1]/button').click()
# 고객센터 전화번호 인증 안내
driver.find_element_by_xpath('/html/body/div[1]/div/div/div[3]/div/div/button').click()
# 종료 확인 팝업
driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div/span[2]/button').click()