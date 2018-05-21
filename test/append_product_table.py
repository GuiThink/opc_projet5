#! /usr/bin/env python3
# coding: utf-8
import requests
import psycopg2
from psycopg2.extras import Json
import urllib.parse


conn = psycopg2.connect(host="localhost", database="openfoodfacts_db", user="postgres", password="postgres")
cursor = conn.cursor()


def append_product_table():
    cursor.execute("SELECT category_name_fr FROM category WHERE id = ROUND(RANDOM() * 29) + 1")

    datas = cursor.fetchall()
    for elem in datas:
        # print(f"{elem}")
        formated_elem = '\n'.join(elem)

        main_api = 'https://fr.openfoodfacts.org/'
        api_ending = '.json'

        category_url = main_api + urllib.parse.urlencode({'category/': formated_elem + api_ending})

        json_data = requests.get(category_url).json()

        # json_status = json_data['status_verbose']
        # print('API Status : ' + json_status)

        try:
            for each in json_data['products']:
                print(f"Product name : {each['product_name_fr']} \nCategory : {each['categories']}  \nNutrition grade : {each['nutrition_grades_tags']} \nStore : {each['stores']} \nCountry : {each['countries']} \n =============")
        except KeyError:
            pass


append_product_table()
