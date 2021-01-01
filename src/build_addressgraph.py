#! /usr/bin/env python
# -*- coding:utf-8 -*-
#=====================================
# Author      : Zhaoyoubiao
# File name   : build_addressgraph.py
# Create date : 2020/12/30 17:01
# IDE         : pycharm
#=====================================
import os
from py2neo import Graph, Node

class AddressGraph:
    def __init__(self):
        self.base_dir = "/data/home/zhaoyoubiao/NLP/text_classification/ner_address/kg_add/kg"
        self.g = Graph(
            host='10.9.47.28',
            http_port=7474,
            user='neo4j',
            password='Zyb5086z'
        )

    def read_nodes(self):
        filenames = os.listdir(self.base_dir)
        # 存储省份、省份和城市隶属关系
        province_name = []
        province_city_relationships = []

        # 储存城市、城市与区县隶属关系
        city_name = []
        city_district_relationshaips = []

        # 存储区县、区县与镇乡街道隶属关系
        district_name = []
        district_street_relationships = []

        # 存储街道镇乡、街道和区域热点隶属关系
        street_name = []
        street_poi_relationships = []

        # 存储POI热点区域
        poi_name = []
        for filename in filenames:
            with open(os.path.join(self.base_dir, filename), 'r', encoding='utf-8') as f:
                datas = f.readlines()
                name = filename.split('.')[0]
                if  name == 'province':
                    for data in datas:
                        data = data.strip().split('\t')
                        if data[0] not in province_name:
                            province_name.append(data[0])
                        if data[1] not in city_name:
                            city_name.append(data[1])
                        r = [data[0], data[1]]
                        if r not in province_city_relationships:
                            province_city_relationships.append(r)
                elif name == 'city':
                    for data in datas:
                        data = data.strip().split('\t')
                        if data[1] not in district_name:
                            district_name.append(data[1])
                        r = [data[0], data[1]]
                        if r not in city_district_relationshaips:
                            city_district_relationshaips.append(r)
                elif name == 'district':
                    for data in datas:
                        data = data.strip().split('\t')
                        if data[1] not in street_name:
                            street_name.append(data[1])
                        r = [data[0], data[1]]
                        if r not in district_street_relationships:
                            district_street_relationships.append(r)

                else:
                    for data in datas:
                        data = data.strip().split('\t')
                        if data[1] not in poi_name:
                            poi_name.append(data[1])
                        r = [data[0], data[1]]
                        if r not in street_poi_relationships:
                            street_poi_relationships.append(r)
        return province_name, province_city_relationships, city_name, city_district_relationshaips, district_name, district_street_relationships, street_name, street_poi_relationships, poi_name

    # 创建节点
    def create_nodes(self, label, nodes):
        count = 0
        for node in nodes:
            node = Node(label, name=node)
            self.g.create(node)
            count += 1
            print(label, count)
        print("create {} node finish!".format(label))

    def create_relationships(self, start_node, end_node, relationships, rel_type, rel_name):
        count = 0
        for relation in relationships:
            p, q = relation[0], relation[1]
            query = "match (p:%s), (q:%s) where p.name='%s' and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                start_node, end_node, p, q, rel_type, rel_name
            )
            try:
                self.g.run(query)
                count += 1
                print(rel_name, count)
            except Exception as e:
                print(e)
        print('create {} relationship finish!'.format(rel_type))

    def create_relationships_opposite(self, start_node, end_node, relationships, rel_type, rel_name):
        count = 0
        for relationship in relationships:
            p, q = relationship[1], relationship[0]
            query = "match (p:%s), (q:%s) where p.name='%s' and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                start_node, end_node, p, q, rel_type, rel_name
            )
            try:
                self.g.run(query)
                count += 1
                print(rel_name, count)
            except Exception as e:
                print(e)
        print('create {} relationship finish!'.format(rel_type))

    def create_graph(self):
        province_name, province_city_relationships, city_name, city_district_relationshaips, district_name, district_street_relationships, \
        street_name, street_poi_relationships, poi_name = self.read_nodes()
        self.create_nodes("province", province_name)
        self.create_nodes("city", city_name)
        self.create_nodes("district", district_name)
        self.create_nodes("street", street_name)
        self.create_nodes("poi", poi_name)

        self.create_relationships("province", "city", province_city_relationships, "province_city", "省属城市")
        self.create_relationships_opposite("city", "province",  province_city_relationships, "city_province", "市省关系")
        self.create_relationships("city", "district", city_district_relationshaips, "city_district", "市区隶属")
        self.create_relationships_opposite("district", "city", city_district_relationshaips, "district_city", "区市关系")
        self.create_relationships("district", "street", district_street_relationships, "district_street", "县镇隶属")
        self.create_relationships_opposite("street", "district", district_street_relationships, "street_district", "镇区关系")
        self.create_relationships("street", "poi", street_poi_relationships, "street_poi", "街道热点隶属")
        self.create_relationships_opposite("poi", "street", street_poi_relationships, "poi_street", "热点街道关系")

if __name__ == '__main__':
    address_graph = AddressGraph()
    address_graph.create_graph()