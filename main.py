from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import os
import re
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import web_io
import csv_io 
import matplotlib.pyplot as plt
import numpy as np

import GetInstanceId as gid
from visualization import by_matplotlib as matvis
from Datanalysis import methodtime as mtime

if __name__ == '__main__':
    method_name = 'Create Subs For OE'
    start_date = datetime.strptime('2023-09-30 00:00:00','%Y-%m-%d %H:%M:%S')
    mtime.analyze_method_times(cloud_test=True, method_name=method_name, start_date=start_date)
    '''
    ## job_id
    TM: 2389
    UM: 67
    MTN: 2248, 2305
    '''
    # mtime.analyze_serial_duration(job_id=67, date='2023-11-28', log=True)