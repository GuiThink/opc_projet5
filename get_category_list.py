#! /usr/bin/env python3
# coding: utf-8

import requests
import psycopg2
from psycopg2.extras import Json

def get_category_list():
    """
    This function sends a GET query to the openfoodfacts API
    to get all the categories.
    Query response is a JSON file.
    """
    main_api = 'https://fr.openfoodfacts.org/categories.json'
    print('Request URL : ' + main_api)
    print('Loading datas...please wait.')

    json_data = requests.get(main_api).json()

    # json_status = json_data['status_verbose']
    # print('API Status : ' + json_status)

    # for each in json_data['tags']:
    #     print(f"category_id : {each['id']} \nname_fr : {each['name']} \nurl_fr : {each['url']}\n----------")

    insert_into_category_table(json_data)


def insert_into_category_table(json_data):

    print('Starting parsing datas...please be patient.')
    for each in json_data['tags']:
        category_id = each['id']
        category_name_fr = each['name']
        # print(category_id)
        # print(category_name_fr)

        datas_to_insert = (category_id, category_name_fr)

        with psycopg2.connect(host="localhost", database="openfoodfacts_db", user="postgres", password="postgres") as conn:
                with conn.cursor() as cursor:
                    query = """
                        INSERT into
                            category
                            (category_id, category_name_fr)
                        VALUES
                            (%s, %s);
                    """
                    cursor.execute(query, datas_to_insert)

                conn.commit()

        print('Datas inserted into the table.')
        print('Done.')


# def read_from_db():
#     cursor.execute("SELECT * FROM category")
#     # data = cursor.fetchall()
#     for row in cursor.fetchall():
#         print(row)


get_category_list()



# def insert_into_table(data):
#     # preparing geometry json data for insertion
#     for item in data:
#         item['geom'] = Json(item['geometry'])
#
#     with psycopg2.connect(database='testdb', user='postgres', password='password', host='localhost') as conn:
#         with conn.cursor() as cursor:
#             query = """
#                 INSERT into
#                     data_load
#                     (iso_code, l_postcode, r_postcode, link_id, geom)
#                 VALUES
#                     (%(iso_code)s, %(l_postcode)s, %(r_postcode)s, %(link_id)s, st_geomfromgeojson(%(geom)s));
#             """
#             cursor.executemany(query, data)
#
#         conn.commit()
