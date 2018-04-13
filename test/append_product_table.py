#! /usr/bin/env python3
# coding: utf-8
import requests
import psycopg2
from psycopg2.extras import Json
import urllib.parse


conn = psycopg2.connect(host="localhost", database="openfoodfacts_db", user="postgres", password="postgres")
cursor = conn.cursor()


def append_product_table():
    cursor.execute("SELECT category_name_fr FROM category")

    datas = cursor.fetchall()
    for elem in datas:
        print(f"{elem}")

        # main_api = 'https://fr.openfoodfacts.org/'
        # api_ending = '.json'
        #
        # category_url = main_api + urllib.parse.urlencode({'category/': elem + api_ending})
        # print('Request URL : ' + category_url)
        #
        # json_data = requests.get(category_url).json()
        #
        # # json_status = json_data['status_verbose']
        # # print('API Status : ' + json_status)
        #
        # for each in json_data['products']:
        #     print(each['product_name_fr'])
        #     print(each['category_tags'])
        #     print(each['nutrition_grades_tags'])
        #     print(each['stores'])
        #     print(each['countries'])


append_product_table()
