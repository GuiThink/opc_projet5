#! /usr/bin/env python3
# coding: utf-8

import psycopg2
import psycopg2.extras
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import requests
import json
import os


def create_database():
    """
    Database creation process
    """
    try:
        conn = psycopg2.connect(host="localhost", user="postgres", password="postgres")
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE openfoodfacts_db ENCODING 'UTF8';")
        conn.commit()
        cursor.close()
        conn.close()
    except psycopg2.ProgrammingError:
        pass


def create_table():
    """
    Tables creation process
    """
    conn = psycopg2.connect(host="localhost", database="openfoodfacts_db", user="postgres", password="postgres")
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS category (category_id VARCHAR(255) UNIQUE NOT NULL, PRIMARY KEY(category_id));")

    cursor.execute("CREATE TABLE IF NOT EXISTS store (store_id VARCHAR(255) UNIQUE NOT NULL, PRIMARY KEY (store_id));")

    cursor.execute("""CREATE TABLE IF NOT EXISTS product 
                      (product_id VARCHAR(255) UNIQUE NOT NULL,
                      product_name_fr VARCHAR(255) NOT NULL,
                      product_nutrition_grade VARCHAR(1) NOT NULL,
                      product_url VARCHAR(255) NOT NULL,
                      store_id VARCHAR(255) NOT NULL REFERENCES store (store_id),
                      category_id VARCHAR(255) NOT NULL REFERENCES category (category_id),
                      PRIMARY KEY (product_id)
                      );
                      """)

    conn.commit()
    cursor.close()
    conn.close()


def get_api_data():
    """
    Retrieves data from api url
    """
    api_url = """https://fr.openfoodfacts.org/cgi/search.pl?action=process&tagtype_0=countries
    &tag_contains_0=contains&tag_0=france&tagtype_1=purchase_places
    &tag_contains_1=contains&tag_1=france&tagtype_2=languages
    &tag_contains_2=contains&tag_2=fran%C3%A7ais
    &sort_by=unique_scans_n&page_size=1000&axis_x=energy
    &axis_y=products_n&action=display&json=1"""
    json_data = requests.get(api_url).json()
    write_json_file(json_data)


def write_json_file(json_data):
    """
    Saves json database dump file on local disk
    """
    with open('json_openfoodfacts_db.json', 'w') as outfile:
        json.dump(json_data, outfile)

    read_from_local_json_file()


def read_from_local_json_file():
    """
    Read json database dump file from local disk
    """
    if os.path.isfile('json_openfoodfacts_db.json'):
        with open('json_openfoodfacts_db.json') as json_data:
            raw_data = json.load(json_data)

            return raw_data


def filter_categories(raw_data):
    """
    Selects fr category id's and apply some filters
    """
    raw_categories = []

    for product in raw_data['products']:
        category_list = product['categories_tags']
        for category in category_list:
            raw_categories.append(category)

    fr_categories = []

    for category in raw_categories:
        if 'fr:' in category:
            fr_categories.append(category)

    keepers = []
    occurrence_limit = 2

    for category in fr_categories:
        if fr_categories.count(category) >= occurrence_limit:
            keepers.append(category)

    return keepers


def remove_duplicates(list_to_clean):
    """
    Removes duplicates from a given list
    """
    unique_data_list = []
    check_list = set()
    for elem in list_to_clean:
        if elem not in check_list:
            unique_data_list.append(elem)
            check_list.add(elem)

    return unique_data_list


def filter_products(raw_data, keepers):
    """
    Uses the raw json file and the list of category keepers (categories with at least 2 or more products)
    to find the products that correspond to these categories and then appends these products details to a product list
    """
    raw_product_list = []

    for product in raw_data['products']:
        category_list = product['categories_tags']

        for cat in category_list:

            if cat in keepers:
                try:
                    product_id = product['id']
                    product_name_fr = product['product_name_fr']
                    product_nutrition_grade = product['nutrition_grades']
                    product_url_fr = product['url']
                    product_store = product['stores_tags'][0]  # takes the first store found

                    raw_product_list.append((product_id, product_name_fr, product_nutrition_grade,
                                         product_url_fr, product_store, cat))
                except (KeyError, IndexError):
                    continue

            else:
                continue

    clean_product_list = []
    check_list = set()

    for elem in raw_product_list:
        product_name = elem[1]
        if product_name not in check_list:
            clean_product_list.append(elem)
            check_list.add(product_name)

    return clean_product_list


def filter_stores(raw_data, keepers):
    """
    Create a list of stores that contains all stores found for each category present in category keepers list
    """
    store_list = []
    for product in raw_data['products']:
        category_list = product['categories_tags']
        # print(category_list)
        for cat in category_list:
            try:
                if cat in keepers:
                    product_store = product['stores_tags']
                    if product_store:
                        store_list.append(product_store)
                    else:
                        continue
                else:
                    continue
            except KeyError:
                pass

    store_keepers = []

    for elem in store_list:
        for each in elem:
            store_keepers.append(each)

    return store_keepers


def insert_into_category(ready_to_go_category_list):
    """
    Import selected categories into PostgreSql table
    """
    data_to_insert = []

    for elem in ready_to_go_category_list:
        split_elem = list(elem.split())
        data_to_insert.append(split_elem)

    with psycopg2.connect(host="localhost", database="openfoodfacts_db", user="postgres", password="postgres") as conn:
        try:
            with conn.cursor() as cursor:
                for each in data_to_insert:
                    cursor.execute("INSERT INTO category (category_id) VALUES (%s)", each)
            print(">> CATEGORY TABLE INFO : datas inserted into table.")
        except psycopg2.IntegrityError:
            print(">> CATEGORY TABLE INFO : PK already exists into table. Ignoring new insert.")
            pass

    conn.commit()
    conn.close()


def insert_into_store(ready_to_go_store_list):
    """
    Insert store list into store table
    """
    data_to_insert = []
    
    for elem in ready_to_go_store_list:
        split_elem = list(elem.split())
        data_to_insert.append(split_elem)

    with psycopg2.connect(host="localhost", database="openfoodfacts_db", user="postgres", password="postgres") as conn:
        try:
            with conn.cursor() as cursor:
                for each in data_to_insert:
                    cursor.execute("INSERT INTO store (store_id) VALUES (%s)", each)
            print(">> STORE TABLE INFO : datas inserted into table.")
        except psycopg2.IntegrityError:
            print(">> STORE TABLE INFO : PK already exists into table. Ignoring new insert.")
            pass

    conn.commit()
    conn.close()


def insert_into_product(ready_to_go_product_list):
    """
    Insert products into product table
    """
    with psycopg2.connect(host="localhost", database="openfoodfacts_db", user="postgres", password="postgres") as conn:
        try:
            with conn.cursor() as cursor:
                for each in ready_to_go_product_list:
                    cursor.execute("""INSERT INTO product 
                                      (product_id, product_name_fr, product_nutrition_grade, 
                                      product_url, store_id, category_id) 
                                      VALUES (%s, %s, %s, %s, %s, %s)""", each)
            print(">> PRODUCT TABLE INFO : datas inserted into table.")
        except psycopg2.IntegrityError:
            print(">> PRODUCT TABLE INFO : PK already exists into table. Ignoring new insert.")
            pass

    conn.commit()
    conn.close()


def read_category_table():
    """
    """
    with psycopg2.connect(host="localhost", database="openfoodfacts_db", user="postgres", password="postgres") as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT category_id FROM category LIMIT 30")
            data = cursor.fetchall()

    return data


def read_store_table():
    """
    """
    with psycopg2.connect(host="localhost", database="openfoodfacts_db", user="postgres", password="postgres") as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT store_id FROM store")
            data = cursor.fetchall()

    return data


def get_products_for_given_category(cat_desc):
    """
    """
    with psycopg2.connect(host="localhost", database="openfoodfacts_db", user="postgres", password="postgres") as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT product.product_id, product.product_name_fr FROM product, category WHERE product.category_id = category.category_id AND category.category_id = %s", cat_desc)
            data = cursor.fetchall()

    return data


def get_all_products():
    """
    """
    with psycopg2.connect(host="localhost", database="openfoodfacts_db", user="postgres", password="postgres") as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM product")
            data = cursor.fetchall()

    return data


def get_chosen_product_details(pdct_id):
    """
    """
    data_to_insert = list(pdct_id.split())

    with psycopg2.connect(host="localhost", database="openfoodfacts_db", user="postgres", password="postgres") as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM product WHERE product_id = %s", data_to_insert)
            data = cursor.fetchall()

    return data


def get_substitute_product_details(pdct_id):
    """
    """
    data_to_insert = list(pdct_id.split())

    with psycopg2.connect(host="localhost", database="openfoodfacts_db", user="postgres", password="postgres") as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM product WHERE product_id = %s", data_to_insert)
            data = cursor.fetchall()

    return data


def main():

    # database and tables creation process
    create_database()
    create_table()

    # data retrieving process
    if not os.path.isfile('json_openfoodfacts_db.json'):
        get_api_data()
    else:
        read_from_local_json_file()

    raw_data = read_from_local_json_file()

    # category filtering process
    category_keepers = filter_categories(raw_data)
    ready_to_go_category_list = sorted(remove_duplicates(category_keepers))

    # product filtering process
    ready_to_go_product_list = sorted(filter_products(raw_data, category_keepers))

    # store filtering process
    store_keepers = filter_stores(raw_data, category_keepers)
    ready_to_go_store_list = sorted(remove_duplicates(store_keepers))

    # inserts process
    insert_into_category(ready_to_go_category_list)
    insert_into_store(ready_to_go_store_list)
    insert_into_product(ready_to_go_product_list)

    # read from db process
    cat_table = read_category_table()
    # sto_table = read_store_table()
    # pdct_table = read_product_table()

    # terminal process

    cat_id = 1

    for category in cat_table:
        print(f"{cat_id} | {category[0]}")
        cat_id += 1

    cat_input = int(input("\n>> Please chose a category and press ENTER : \n"))
    cat_index = cat_input -1
    cat_desc = cat_table[cat_index]

    print(f"\nYou have selected category {cat_input} | {cat_table[cat_index][0]} \n")


    product_list = get_products_for_given_category(cat_desc)

    pdct_id = 1
    for pdct in product_list:
        print(f"{pdct_id} | {pdct[1]}")
        pdct_id += 1

    pdct_input = int(input("\n>> Please chose a product and press ENTER : \n"))
    pdct_index = pdct_input -1
    pdct_id = product_list[pdct_index][0]

    print(f"\nYou have selected product {pdct_input} | {product_list[pdct_index][1]} \n")


    all_products = get_all_products()
    found_substitute = get_chosen_product_details(pdct_id)


    # substitute_pdct = get_substitute_product_details(pdct_id) # à changer par l'id du substitut
    # for pdct_attribute in substitute_pdct:
    #     print("|||||||||||||| SUBSTITUTE ||||||||||||||")
    #     print(f">> Substitute product advised : {pdct_attribute[1]} \n>> Nutritional grade : {pdct_attribute[2]} \n>> URL : {pdct_attribute[3]}  \n>> Where to buy : {pdct_attribute[4]}")
    #     print("||||||||||||||||||||||||||||||||||||||||\n")

if __name__ == "__main__":
    main()