#! /usr/bin/env python3
# coding: utf-8

import requests
import psycopg2
from psycopg2.extras import Json


def get_store_list():
    """
    This function sends a GET query to the openfoodfacts API
    to get all the stores.
    Query response is a JSON file.
    """
    main_api = 'https://world.openfoodfacts.org/stores.json'
    print('Request URL : ' + main_api)
    print('>> 1/3 - LOADING DATAS FROM API. PLEASE WAIT...')

    json_data = requests.get(main_api).json()

    insert_into_store_table(json_data)


def insert_into_store_table(json_data):
    """
    This function connects to the database, Parse targeted datas
    and Insert them into the defined table.
    """
    print('>> 2/3 - START INSERTING DATAS INTO TABLE. PLEASE WAIT...')
    with psycopg2.connect(host="localhost", database="openfoodfacts_db", user="postgres", password="postgres") as conn:

        datas_to_insert = []

        for each in json_data['tags']:
            store_id = each['id']
            store_desc_fr = each['name']
            datas_to_insert.append((store_id, store_desc_fr))
            # print(store_id)
            # print(store_desc_fr)

        with conn.cursor() as cursor:
            query = """
                INSERT INTO
                    store
                    (store_id, store_desc_fr)
                VALUES
                    (%s, %s);
            """
            cursor.executemany(query, datas_to_insert)

        conn.commit()

    print('>> 3/3 - DATAS INSERTED INTO TABLE. ALL DONE.')


get_store_list()


# def read_from_db():
#     cursor.execute("SELECT * FROM category")
#     # data = cursor.fetchall()
#     for row in cursor.fetchall():
#         print(row)
