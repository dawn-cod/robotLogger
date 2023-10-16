import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from datetime import datetime

def get_instance_id():
    id_list = ['6597865']
    return id_list

def get_outputxml(instance_id):
    url = f"http://10.10.169.17:9443/cos-cloudtest/autotest/{instance_id}/report/output.xml"
    response = requests.get(url)
    return response.text

def query_method_time(method:str, instance_id:str) -> list:
    xmltext = get_outputxml(instance_id)
    # print(xmltext)
    root = ET.fromstring(xmltext)
    allele = root.findall(f".//kw[@name='{method}']")
    for ele in allele:
        eles = ele.findall(f"msg[@timestamp]")
        starttime = datetime.strptime(eles[0].attrib['timestamp'],'%Y%m%d %H:%M:%S.%f')
        endtime = datetime.strptime(eles[1].attrib['timestamp'],'%Y%m%d %H:%M:%S.%f')
        print(endtime-starttime)
        # 上面这个拿到的时间还是个str，还得转成date再减


if __name__ == '__main__':
    instance_id_list = get_instance_id()
    for instance_id in instance_id_list:
        method_time = query_method_time('Enter Specific Menu', instance_id)

