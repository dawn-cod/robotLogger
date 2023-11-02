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
import web_io
import csv_io 
import matplotlib.pyplot as plt
import numpy as np

import GetInstanceId as gid
from visualization import by_matplotlib as matvis


def query_method_time(method:str, instance_id:str) -> list:
    '''根据给定的单个实例，返回一组用例中某个关键字的用时列表
    

    return:
        duration_and_starttime = [{'duration': duration, 'starttime': starttime},{},{}...]
    '''
    xmltext = web_io.get_outputxml(instance_id)
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
    
    # instance_ids = gid.get_instance_id(datetime.strptime('2023-10-18 00:00:00','%Y-%m-%d %H:%M:%S'))

    # method_times = get_all_methods_time(instance_ids, method_name)
    
    # csv_io.save_method_times_to_csv(method_name, method_times)
    method_times = csv_io.read_csv_to_scatter_data(method_name)

    matvis.visualize_method_duration(method_times, method_name)
    

