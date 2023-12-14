import sys 
sys.path.append("..") 
import xml.etree.ElementTree as ET
import datetime
import numpy as np

import database_connection as db_connection
import web_io
import csv_io 
import GetInstanceId as gid
from visualization import by_matplotlib as matvis

def analyze_method_times(method_name, cloud_test, start_date=None, end_date=None):
    if cloud_test:
        instance_ids = gid.get_instance_id(start_date, end_date)
        method_times = get_all_methods_time(instance_ids, method_name)
        csv_io.save_method_times_to_csv(method_name, method_times)
        # method_times = csv_io.read_csv_to_scatter_data(method_name)
        matvis.visualize_method_duration(method_times, method_name)
    else:
        # 不从云测获取的还没写
        pass

def analyze_serial_duration(date, job_id=2389, log=False):
    Con = db_connection.Connection()
    sql ="""select ti.project_inst_id from zcm_devspace.autotest_job_task_inst ti
            where ti.job_inst_id in(
                select ji.id from zcm_devspace.autotest_job_inst ji
	                where ji.job_id = %s
		              and DATE_FORMAT(ji.create_date, '%%Y-%%m-%%d') = %s)"""
    instance_ids = tuple(element for subtuple in Con.exc(sql, (job_id, date,)) for element in subtuple) 
    total_duration = get_all_serial_duration(instance_ids, log=log)
    print(total_duration)

############################################################################
############################# 入参为Instance ID #############################
############################################################################

def get_all_methods_time(instance_ids:list, method_name:str):
    '''从给定的所有xml文件获取所有 指定关键字 的耗时
    
    args:

    returns:
        methods_times = [{},{},...]
    '''
    method_times = []
    for instance_id in instance_ids:
        xmltext = web_io.get_outputxml(instance_id['current_instance_id'])
        duration_and_starttime = query_method_time(method_name, xmltext)
        if duration_and_starttime is None:
            continue
        for single_case in duration_and_starttime:
            method_times.append({'method_time': single_case['duration'], 
                                 'create_date': single_case['starttime'], 
                                 'is_success':  single_case['is_success']})
    return method_times

def get_all_serial_duration(instance_ids:list, log=False):
    total_duration = datetime.timedelta(seconds=0)
    for instance_id in instance_ids:
        if log:
            print(f"[instance_id]{instance_id} start")
        xmltext = web_io.get_outputxml(instance_id)
        if xmltext:
            total_duration += query_serial_duration(xmltext, log=log)
        if log:
            print(f"[instance_id]{instance_id} END total_time is {total_duration}")
    return total_duration


############################################################################
############################## #入参为xmltext ###############################
############################################################################

def query_method_time(method:str, xmltext:str) -> list:
    '''根据给定的xmltest，返回一组用例中某个关键字的用时列表
    
    return:
        duration_and_starttime = [{'duration': duration, 'starttime': starttime},{},{}...]
    '''
    try:
        root = ET.fromstring(xmltext)
    except Exception as e:
        print(f"xmltext is\n{xmltext}")
        return None
        raise e
    duration_and_starttime = []
    allele = root.findall(f".//kw[@name='{method}']")
    for ele in allele:
        eles = ele.findall(f"msg[@timestamp]")
        starttime = datetime.datetime.strptime(eles[0].attrib['timestamp'],'%Y%m%d %H:%M:%S.%f')
        endtime = datetime.datetime.strptime(eles[1].attrib['timestamp'],'%Y%m%d %H:%M:%S.%f')
        duration = endtime - starttime
        # print(f"duration is {duration}")
        status_ele = ele.findall(f"status[@status]")
        status = status_ele[0].attrib['status']
        is_success = True if status == "PASS" else (False if status == "FAIL" else None)
        duration_and_starttime.append({'duration': duration, 'starttime': starttime, 'is_success': is_success})
    return duration_and_starttime

def query_serial_duration(xmltext: str, log=False) -> float:
    try:
        root = ET.fromstring(xmltext)
    except Exception as e:
        print(f"xmltext is\n{xmltext}")
        return None
        raise e
    totaltime = datetime.timedelta(seconds=0)
    for ele in root.findall(".//test/..[@id]"):
        test_name = ele.find(".//test").attrib['name']
        status_ele = ele.find("./status")
        starttime = datetime.datetime.strptime(status_ele.attrib['starttime'],'%Y%m%d %H:%M:%S.%f')
        endtime = datetime.datetime.strptime(status_ele.attrib['endtime'],'%Y%m%d %H:%M:%S.%f')
        duration = endtime - starttime
        if log:
            print(f"\t[TEST]{test_name} costs {duration}")
        totaltime += duration
    return totaltime


