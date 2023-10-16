from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options

starttime = time.time()

options = Options()
options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options=options)


driver.get("https://dev.iwhalecloud.com/portal/main.html?portalId=3")

print(f"[TIME INSPECT] startup uses {time.time()-starttime} seconds")

driver.implicitly_wait(2)

print(f"[TIME INSPECT] findele starts at {time.time()-starttime} seconds")
name_ele = driver.find_element(By.XPATH, "//input[@name='username' and @placeholder='工号']")
print(f"[TIME INSPECT] findele ends at {time.time()-starttime} seconds")

print(name_ele)
print(name_ele.get_attribute("class"))

print(f"[TIME INSPECT] sendkeys ends at {time.time()-starttime} seconds")
name_ele.send_keys("0027026730")
print(f"[TIME INSPECT] findele starts at {time.time()-starttime} seconds")
password_ele = driver.find_element(by=By.NAME, value="edt_pwd")
print(f"[TIME INSPECT] findele ends at {time.time()-starttime} seconds")
password_ele.send_keys("WZH11235813hAOJ!")

login_ele = driver.find_element(by=By.CLASS_NAME, value="loginBtn")
login_ele.click()



# driver.quit()