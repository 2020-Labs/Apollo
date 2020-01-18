from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

base_url = "http://www.baidu.com"
#driver = webdriver.Firefox()
driver = webdriver.Chrome()
driver.maximize_window()
driver.get(base_url)
print(driver.title)
driver.find_element_by_id("kw").clear()
driver.find_element_by_id("kw").send_keys("Python")
driver.find_element_by_id("su").click()
time.sleep(5)
print(driver.title)

driver.find_element_by_id("kw").clear()
driver.find_element_by_id("kw").send_keys("Android")
driver.find_element_by_id("su").click()
time.sleep(10)
print(driver.title)
driver.quit()