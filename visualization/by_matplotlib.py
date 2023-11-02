import csv
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

def visualize_method_duration(method_times, method_name=None):
    transferred_data = []
    for raw_dict in method_times:
        # print(f"type(raw_dict['create_date']) is {type(raw_dict['create_date'])}")
        brief_create_date = int(datetime.strftime(raw_dict['create_date'],'%y%m%d'))
        method_time = raw_dict['method_time'] if type(raw_dict['method_time'])==float else raw_dict['method_time'].total_seconds()
        print(f"brief_create_date is  {brief_create_date}")
        print(f"raw_dict[method_time] is  {method_time}")
        transferred_data.append({'method_time':method_time, 'create_date':brief_create_date})
    ready = [[x['method_time'] for x in transferred_data], [x['create_date'] for x in transferred_data]]
    plt.scatter(ready[1], ready[0])
    plt.rcParams["font.sans-serif"]=["SimHei"] #设置字体
    plt.ticklabel_format(style='plain')
    plt.ylabel('方法耗时（秒）')
    plt.xlabel('日期（年月日）')
    plt.show()  