#! /usr/bin/env python
# -*- coding:utf-8 -*-
#=====================================
# Author      : Zhaoyoubiao
# File name   : process_data_kg.py
# Create date : 2020/12/30 15:20
# IDE         : pycharm
#=====================================
import os
import pandas as pd
from tqdm import tqdm
base_dir = "./data/kg_data"

# 读取配置表
def read_district_street():
    data_dir = os.path.join(base_dir, 'district_street.txt')
    district_street = {}
    with open(data_dir, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip().split('\t')
            district = line[0]
            streets = line[1].split('、')
            district_street[district] = streets
    return district_street


# 提取省市区镇和小区、医院、商场、写字楼、学校
def get_address():
    source_dir = os.path.join(base_dir, "shanghai_address.csv")
    datas = pd.read_csv(source_dir, encoding='gb18030')
    result = []
    district_street = read_district_street()
    for i in tqdm(range(len(datas))):
        data_dict = []
        if datas['district'][i] != '(NULL)' and datas['street'][i] != '(NULL)' and datas['poi'][i] != '(NULL)':
            if datas['district'][i] in district_street:
                streets = district_street[datas['district'][i]]
                for street in streets:
                    if street in datas['street'][i]:
                        data_dict.append('上海')
                        data_dict.append('上海市')
                        data_dict.append(datas['district'][i])
                        data_dict.append(street)
                        data_dict.append(datas['poi'][i])
                        if data_dict not in result:
                            result.append(data_dict)
                            break

    with open(os.path.join(base_dir, 'kg_address.txt'), 'w', encoding='utf-8') as f:
        for res in result:
            f.write(res[0] + '\t' + res[1] + '\t' + res[2] + '\t' + res[3] + '\t' + res[4])
            f.write('\n')

# generator kg data
def generator_kg_data():
    with open(os.path.join(base_dir, 'kg_address.txt'), 'r', encoding='utf-8') as f:
        datas = f.readlines()
        data_province = []
        data_city = []
        data_district = []
        data_street = []
        for data in datas:
            lines = data.strip().split('\t')
            province = [lines[0], lines[1]]
            if province not in data_province:
                data_province.append(province)
            city = [lines[1], lines[2]]
            if city not in data_city:
                data_city.append(city)
            district = [lines[2], lines[3]]
            if district not in data_district:
                data_district.append(district)
            street = [lines[3], lines[4]]
            if street not in data_street:
                data_street.append(street)
        with open(os.path.join(base_dir, 'kg/province.txt'), 'w', encoding='utf-8') as f:
            for province in data_province:
                f.write(province[0] + '\t' + province[1] + '\n')
        with open(os.path.join(base_dir, 'kg/city.txt'), 'w', encoding='utf-8') as f:
            for city in data_city:
                f.write(city[0] + '\t' + city[1] + '\n')

        with open(os.path.join(base_dir, 'kg/district.txt'), 'w', encoding='utf-8') as f:
            for district in data_district:
                f.write(district[0] + '\t' + district[1] + '\n')
        with open(os.path.join(base_dir, 'kg/street.txt'), 'w', encoding='utf-8') as f:
            for street in data_street:
                f.write(street[0] + '\t' + street[1] + '\n')

if __name__ == '__main__':
    get_address()
    generator_kg_data()