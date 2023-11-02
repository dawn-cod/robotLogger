import requests

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