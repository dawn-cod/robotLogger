from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import re
from datetime import datetime

def get_instance_id(start_date, end_date=None):
    starttime = time.time()

    options = Options()
    options.page_load_strategy = 'eager'
    driver = webdriver.Chrome(options=options)


    driver.get("https://dev.iwhalecloud.com/portal/main.html?portalId=3")

    print(f"[TIME INSPECT] startup uses {time.time()-starttime} seconds")

    driver.implicitly_wait(10)

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
    ################################登录完成################################
    time.sleep(4)
    menu_ele = driver.find_element(by=By.XPATH, value="//span[@class='iconfont icon-menu-list portal__nav_icon js-menu']")
    menu_ele.click()

    driver.find_element(by=By.ID, value="searchMenuInput").send_keys('我的研发空间')
    time.sleep(1)
    specific_menu_ele = driver.find_element(by=By.XPATH, value="//dd//*[@menuname='我的研发空间']")
    ActionChains(driver).double_click(specific_menu_ele).perform()
    time.sleep(1)
    #############################进入我的研发空间#############################

    project_ele = driver.find_element(by=By.XPATH, value="//td[@title='TM_CD_AutoTest']")
    ActionChains(driver).double_click(project_ele).perform()
    time.sleep(1)
    project_ele = driver.find_element(by=By.XPATH, value="//td[@title='TM_CD_AllCases_TMPass']")
    ActionChains(driver).double_click(project_ele).perform()
    time.sleep(1)
    ###############################进入具体项目###############################
    instance_id = []
    is_earlier_than_startdate = False
    triangles_eles = driver.find_elements(by=By.XPATH,value="//div[contains(@class,'treeclick')]")
    for triangle_ele in triangles_eles:
        triangle_ele.click()
        time.sleep(1)
        tr_eles = driver.find_elements(by=By.XPATH, value="//div[@class='ui-tabs-panel' and @menuid]//tr[@id and not(contains(@style, 'display: none;'))][descendant::button[contains(text(), '实例详情')]]")
        print(len(tr_eles))
        for tr_ele in tr_eles:
            create_date_ele = tr_ele.find_element(by=By.XPATH, value="td[contains(@aria-describedby,'createDate')]")
            create_date = datetime.strptime(create_date_ele.get_attribute('title'),'%Y-%m-%d %H:%M:%S')
            print((create_date - start_date).total_seconds())
            if (create_date - start_date).total_seconds() < 0:
                driver.quit()
                return instance_id
            current_instance_id = re.search("\d{7}", tr_ele.get_attribute('id')).group()
            # print(f"current_instance_id is {current_instance_id}")
            instance_id.append({'create_date':create_date, 'current_instance_id':current_instance_id})
        triangle_ele.click()
    
    driver.quit()
    return instance_id


# startdate = datetime.strptime('2023-10-11 12:00:00','%Y-%m-%d %H:%M:%S')
# get_instance_id(startdate)
