#! /usr/bin/env python3
# coding: utf-8
import requests
import psycopg2
from psycopg2.extras import Json
import urllib.parse
from random import randint


conn = psycopg2.connect(host="localhost", database="openfoodfacts_db", user="postgres", password="postgres")
cursor = conn.cursor()


def get_table_entry_count():
    """
    Connects to category table to get total entry count
    """
    cursor.execute("SELECT COUNT(*) FROM category")
    entry_count = cursor.fetchone()[0]
    print(f"There is a total of {entry_count} entries in the category table.")
    generate_rand_cat_list(entry_count)


def generate_rand_cat_list(entry_count):
    """
    Based on total entry count, generates a random list of id's in a chosen range
    """
    rand_cat_id_list = [randint(0, entry_count) for p in range(0, 10)]
    print(f"Random id list : {rand_cat_id_list}")
    get_category_id_list(rand_cat_id_list)


def get_category_id_list(id_list):
    """
    Create a list with categories id's that will be used in the terminal and api requests
    """
    select_query = "SELECT category_id FROM category WHERE id = "

    for id in id_list:
        full_query = select_query + str(id)
        cursor.execute(full_query)
        category_id = cursor.fetchall()
        print(category_id)
        # print(list(cursor.fetchall()))


# def get_products(category_id):
#     """
#     """
#     main_api = 'https://fr.openfoodfacts.org/'
#     api_ending = '.json'
#
#     category_url = main_api + urllib.parse.urlencode({'category/': category_id + api_ending})
#     print('Request URL : ' + category_url)

    # json_data = requests.get(category_url).json()
    #
    # for each in json_data['products']:
    #     print(each['product_name_fr'])


    # with conn.cursor() as cursor:
    #     query = """
    #         SELECT
    #             category_name_fr
    #         FROM
    #             category
    #         WHERE
    #             id = %s);
    #     """
    #     cursor.executemany(query, datas_to_insert)


    # cursor.execute("SELECT category_name_fr FROM category WHERE id = ROUND(RANDOM() * 29) + 1") #
    #
    # datas = cursor.fetchall()
    # for elem in datas:
    #     # print(f"{elem}")
    #     formated_elem = '\n'.join(elem)
    #     print(formated_elem)


        # main_api = 'https://fr.openfoodfacts.org/'
        # api_ending = '.json'
        #
        # category_url = main_api + urllib.parse.urlencode({'category/': formated_elem + api_ending})
        #
        # json_data = requests.get(category_url).json()
        #
        # # json_status = json_data['status_verbose']
        # # print('API Status : ' + json_status)
        #
        # try:
        #     for each in json_data['products']:
        #         print(f"Product name : {each['product_name_fr']} \nCategory : {each['categories']}  \nNutrition grade : {each['nutrition_grades_tags']} \nStore : {each['stores']} \nCountry : {each['countries']} \n =============")
        # except KeyError:
        #     pass


get_table_entry_count()
