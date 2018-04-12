#! /usr/bin/env python3
# coding: utf-8

import requests
import psycopg2
from psycopg2.extras import Json


def get_nutrition_grade_list():
    """
    This function sends a GET query to the openfoodfacts API
    to get all the nutrition grades.
    Query response is a JSON file.
    """
    main_api = 'https://world.openfoodfacts.org/nutrition-grades.json'
    print('Request URL : ' + main_api)
    print('>> 1/3 - LOADING DATAS FROM API. PLEASE WAIT...')

    json_data = requests.get(main_api).json()

    # for each in json_data['tags']:
    #     print(f"category_id : {each['id']} \nname_fr : {each['name']} \nurl_fr : {each['url']}\n----------")

    insert_into_nutrition_grade_table(json_data)


def insert_into_nutrition_grade_table(json_data):
    """
    This function connects to the database, Parse targeted datas
    and Insert them into the defined table.
    """
    print('>> 2/3 - START INSERTING DATAS INTO TABLE. PLEASE WAIT...')
    with psycopg2.connect(host="localhost", database="openfoodfacts_db", user="postgres", password="postgres") as conn:

        datas_to_insert = []

        for each in json_data['tags']:
            nutrition_grade_id = each['id']
            nutrition_grade_desc = each['name']
            if 'a' or 'b' or 'c' or 'd' or 'e' in nutrition_grade_id:
                datas_to_insert.append((nutrition_grade_id, nutrition_grade_desc))
            # print(category_id)
            # print(category_name_fr)

        with conn.cursor() as cursor:
            query = """
                INSERT INTO
                    nutrition_grade
                    (nutrition_grade_id, nutrition_grade_desc)
                VALUES
                    (%s, %s);
            """
            cursor.executemany(query, datas_to_insert)

        conn.commit()

    print('>> 3/3 - DATAS INSERTED INTO TABLE. ALL DONE.')


get_nutrition_grade_list()


# def read_from_db():
#     cursor.execute("SELECT * FROM category")
#     # data = cursor.fetchall()
#     for row in cursor.fetchall():
#         print(row)
