from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

base_url = "http://www.csdn.net"
#driver = webdriver.Firefox()
driver = webdriver.Chrome()
#driver = webdriver.PhantomJS()
driver.maximize_window()
driver.get(base_url)
print(driver.title)
page_source = driver.page_source
with open('d:\csdn.html', mode='w', encoding='utf-8') as file:
    file.writelines(page_source)
    file.close()

driver.find_element_by_id("toolber-keyword").clear()
driver.find_element_by_id("toolber-keyword").send_keys("Python")
time.sleep(2)
driver.find_element_by_id("toolber-keyword").send_keys(Keys.ENTER)

time.sleep(1)
print(driver.title)
driver.save_screenshot('d:\csdn.png')
driver.get_screenshot_as_file('d:\\aaa.png')

driver.quit()