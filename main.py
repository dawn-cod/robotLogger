from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import re
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from datetime import datetime
import GetInstanceId
import csv
import matplotlib.pyplot as plt
import numpy as np

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

def get_outputxml(instance_id):
    url = f"http://10.10.169.17:9443/cos-cloudtest/autotest/{instance_id}/report/output.xml"
    response = requests.get(url)
    return response.text

def query_method_time(method:str, instance_id:str) -> list:
    xmltext = get_outputxml(instance_id)
    # print(xmltext)
    try:
        root = ET.fromstring(xmltext)
    except Exception as e:
        print(f"xmltext is\n{xmltext}")
        return None
        # raise e
    allele = root.findall(f".//kw[@name='{method}']")
    for ele in allele:
        eles = ele.findall(f"msg[@timestamp]")
        starttime = datetime.strptime(eles[0].attrib['timestamp'],'%Y%m%d %H:%M:%S.%f')
        endtime = datetime.strptime(eles[1].attrib['timestamp'],'%Y%m%d %H:%M:%S.%f')
        duration = endtime-starttime
        print(f"duration is {duration}")
        return duration
        # 上面这个拿到的时间还是个str，还得转成date再减

def visualize_method_duration(method_times, method_name=None):
    transferred_data = []
    for raw_dict in method_times:
        brief_create_date = int(datetime.strftime(raw_dict['create_date'],'%y%m%d'))
        method_time = raw_dict['method_time'].total_seconds()
        print(f"brief_create_date is  {brief_create_date}")
        print(f"raw_dict[method_time] is  {method_time}")
        transferred_data.append({'method_time':method_time, 'create_date':brief_create_date})
    ready = [[x['method_time'] for x in transferred_data], [x['create_date'] for x in transferred_data]]
    plt.scatter(ready[0], ready[1])
    plt.show()  

def save_to_csv(method_name, method_times):
    with open(f'[Time Inspect] {method_name}.csv', 'w', newline='') as csvfile:
        fieldnames = ['method_time', 'create_date']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for single_dict in method_times:
            writer.writerow(single_dict)

if __name__ == '__main__':
    method_name = 'Enter Specific Menu'
    # 其实只会保留最近两个星期的记录
    instance_ids = get_instance_id(datetime.strptime('2023-10-05 00:00:00','%Y-%m-%d %H:%M:%S'))
    method_times = []
    for instance_id in instance_ids:
        method_time = query_method_time(method_name, instance_id['current_instance_id'])
        if method_time is None:
            continue
        method_times.append({'method_time':method_time, 'create_date':instance_id['create_date']})
    # print(method_times)
    save_to_csv(method_name, method_times)
    visualize_method_duration(method_times, method_name)
    

