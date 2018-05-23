#! /usr/bin/env python3
# coding: utf-8

import psycopg2
import requests
import json
import os
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


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
    cursor.execute("CREATE TABLE IF NOT EXISTS category (category_id TEXT PRIMARY KEY NOT NULL);")
    cursor.execute("""CREATE TABLE IF NOT EXISTS product 
                      (product_id VARCHAR(100) PRIMARY KEY NOT NULL, 
                      category_id VARCHAR(100) NOT NULL, 
                      product_name_fr VARCHAR(100) NOT NULL, 
                      nutrition_grade_id VARCHAR(14) NOT NULL, 
                      product_url_fr TEXT NOT NULL);
                      """)
    cursor.execute("""CREATE TABLE IF NOT EXISTS nutrition_grade 
                      (nutrition_grade_id VARCHAR(14) PRIMARY KEY NOT NULL, 
                      nutrition_grade_desc TEXT NOT NULL);
                      """)
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS store (store_id TEXT PRIMARY KEY NOT NULL, store_desc_fr TEXT NOT NULL);")
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
    &sort_by=unique_scans_n&page_size=500&axis_x=energy
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
    all_categories = []

    for product in raw_data['products']:
        category_list = product['categories_tags']
        for category in category_list:
            all_categories.append(category)

    all_french_categories = []

    for category in all_categories:
        if 'fr:' in category:
            all_french_categories.append(category)

    return all_french_categories


def remove_empty_categories(all_french_categories):
    """
    Makes sure not to select categories with not enough related products in it
    """
    keepers = []
    occurrence_limit = 2
    for category in all_french_categories:
        if all_french_categories.count(category) >= occurrence_limit:
            keepers.append(category)

    return keepers


def remove_duplicates(keepers):
    """
    Removes duplicates from categories list
    """
    clean_french_categories = []
    check_list = set()
    for category in keepers:
        if category not in check_list:
            clean_french_categories.append(category)
            check_list.add(category)

    return clean_french_categories


def import_into_categories(clean_french_categories):
    """
    Import selected categories into PostgreSql table
    """
    data = []
    for elem in clean_french_categories:
        split_elem = tuple(elem.split())
        data.append(split_elem)
    # print(data)
    with psycopg2.connect(host="localhost", database="openfoodfacts_db", user="postgres", password="postgres") as conn:
        try:
            with conn.cursor() as cursor:
                cursor.executemany("INSERT INTO category (category_id) VALUES (%s)", data)
        except psycopg2.IntegrityError:
            print(""">> Data integrity threat ! PK already exists inside table ! 
No modification applied to current data. Thank you.""")
            pass
    conn.commit()
    conn.close()


def import_stores():
    pass


def filter_products(raw_data, keepers):
    """
    Uses the raw json file and the list of category keepers (categories with at least 2 or more products)
    to find the products that correspond to these categories and then appends these products details to a product list
    """
    product_list = []
    for product in raw_data['products']:
        category_list = product['categories_tags']
        #print(category_list)
        for each in category_list:
            try:
                if each in keepers:
                    product_id = product['id']
                    product_name_fr = product['product_name_fr']
                    product_category_id = product['categories_tags']
                    product_detail = []
                    category_group = []

                    for each in product_category_id:
                        if 'fr:' in each:
                            category_group.append(each)
                    #print(product_id, product_category_id, product_name_fr)

                    product_detail.append(product_id)
                    product_detail.append(product_name_fr)
                    product_detail.append(category_group)

                    product_list.append(product_detail)
                else:
                    continue
            except KeyError:
                pass

    #print(product_list)
    return product_list


def main():
    create_database()
    create_table()

    if not os.path.isfile('json_openfoodfacts_db.json'):
        get_api_data()
    else:
        read_from_local_json_file()

    raw_data = read_from_local_json_file()
    all_french_categories = filter_categories(raw_data)
    keepers = remove_empty_categories(all_french_categories)
    clean_french_categories = remove_duplicates(keepers)
    import_into_categories(clean_french_categories)

    filter_products(raw_data, keepers)

if __name__ == "__main__":
    main()
