from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import os
import re
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from datetime import datetime
import GetInstanceId
import csv
import matplotlib.pyplot as plt
import numpy as np

import GetInstanceId as gid
from visualization import by_matplotlib as matvis

def get_outputxml(instance_id):
    '''
    拿到指定instance_id的xml

    每次从尝试从同目录的文件夹xmlfiles中寻找${instance_id}.xml, 如果没有再去get, get到立刻保存到xmlfiles文件夹中
    '''
    # 构建本地文件路径
    file_path = os.path.join("xmlfiles", f"{instance_id}.xml")
    # 检查本地文件是否存在
    try:
        if os.path.isfile(file_path): 
            with open(file_path, "r", encoding='UTF-8', errors='ignore') as file:
                return file.read()
    except Exception as e:
        print(f"ERROR when reading local xml {instance_id}.xml")
        raise e
    # 如果本地文件不存在，则发送GET请求获取数据
    url = f"http://10.10.169.17:9443/cos-cloudtest/autotest/{instance_id}/report/output.xml"
    response = requests.get(url)
    # 检查请求是否成功
    if response.status_code == 200:
        # 将获取到的数据保存到本地文件
        with open(file_path, "w") as file:
            file.write(response.text)
        return response.text
    # 请求失败时返回空字符串或其他适当的错误处理
    return ""

def query_method_time(method:str, instance_id:str) -> list:
    '''根据给定的单个实例，返回一组用例中某个关键字的用时列表
    

    return:
        duration_and_starttime = [{'duration': duration, 'starttime': starttime},{},{}...]
    '''
    xmltext = get_outputxml(instance_id)
    # print(xmltext)
    try:
        root = ET.fromstring(xmltext)
    except Exception as e:
        print(f"xmltext is\n{xmltext}")
        return None
        # raise e
#############################################################
    duration_and_starttime = []
    allele = root.findall(f".//kw[@name='{method}']")
    for ele in allele:
        eles = ele.findall(f"msg[@timestamp]")
        starttime = datetime.strptime(eles[0].attrib['timestamp'],'%Y%m%d %H:%M:%S.%f')
        endtime = datetime.strptime(eles[1].attrib['timestamp'],'%Y%m%d %H:%M:%S.%f')
        duration = endtime-starttime
        print(f"duration is {duration}")
        duration_and_starttime.append({'duration': duration, 'starttime': starttime})
    return duration_and_starttime

def save_method_times_to_csv(method_name, method_times):
    '''将关键字耗时信息保存进csv中'''
    with open(f'[Time Inspect] {method_name}.csv', 'w', newline='') as csvfile:
        fieldnames = ['method_time', 'create_date']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for single_dict in method_times:
            single_dict = single_dict.copy()
            single_dict['method_time'] = single_dict['method_time'].total_seconds()
            single_dict['create_date'] = datetime.strftime(single_dict['create_date'], '%Y-%m-%d %H:%M:%S.%f')
            writer.writerow(single_dict)

def read_csv_to_scatter_data(method_name):
    with open(f'[Time Inspect] {method_name}.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        method_times = []
        for row in reader:
            current_method_time = datetime.strptime(row['method_time'], '%H:%M:%S.%f')
            current_create_date = datetime.strptime(row['create_date'], '%Y-%m-%d %H:%M:%S.%f')
            method_times.append({'method_time':current_method_time, 'create_date':current_create_date})
        print(f"method_times is \n{method_times}")
        return method_times

def get_all_methods_time(instance_ids, method_name):
    '''从给定的所有xml文件获取所有 指定关键字 的耗时
    
    args:

    returns:
        methods_times = [{},{},...]
    '''
    method_times = []
    for instance_id in instance_ids:
        duration_and_starttime = query_method_time(method_name, instance_id['current_instance_id'])
        if duration_and_starttime is None:
            continue
        for single_case in duration_and_starttime:
            method_times.append({'method_time':single_case['duration'], 'create_date':single_case['starttime']})
    return method_times

if __name__ == '__main__':
    method_name = 'Create Subs For OE'
    
    instance_ids = gid.get_instance_id(datetime.strptime('2023-10-18 00:00:00','%Y-%m-%d %H:%M:%S'))

    method_times = get_all_methods_time(instance_ids, method_name)
    
    # save_method_times_to_csv(method_name, method_times)
    # method_times = read_csv_to_scatter_data(method_name)

    matvis.visualize_method_duration(method_times, method_name)
    

