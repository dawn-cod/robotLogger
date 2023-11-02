import csv
from datetime import datetime

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
            current_method_time = float(row['method_time'])
            current_create_date = datetime.strptime(row['create_date'], '%Y-%m-%d %H:%M:%S.%f')
            method_times.append({'method_time':current_method_time, 'create_date':current_create_date})
        print(f"method_times is \n{method_times}")
        return method_times