#! /usr/bin/env python3
# coding: utf-8

import psycopg2
import requests
import json
import os
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import sys


def get_api_data():
    """
    Retrieves data from api url
    """
    api_url = "https://fr.openfoodfacts.org/cgi/search.pl?action=process&tagtype_0=countries&tag_contains_0=contains&tag_0=france&tagtype_1=purchase_places&tag_contains_1=contains&tag_1=france&tagtype_2=languages&tag_contains_2=contains&tag_2=fran%C3%A7ais&sort_by=unique_scans_n&page_size=100&axis_x=energy&axis_y=products_n&action=display&json=1"
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
            data = json.load(json_data)
            select_categories(data)


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
    cursor.execute("CREATE TABLE IF NOT EXISTS category (id SERIAL PRIMARY KEY, category_id TEXT NOT NULL, category_name_fr TEXT NOT NULL);")
    cursor.execute("CREATE TABLE IF NOT EXISTS product (product_id VARCHAR(100) PRIMARY KEY NOT NULL, category_id VARCHAR(100) NOT NULL, product_name_fr VARCHAR(100) NOT NULL, nutrition_grade_id VARCHAR(14) NOT NULL, product_url_fr TEXT NOT NULL);")
    cursor.execute("CREATE TABLE IF NOT EXISTS nutrition_grade (nutrition_grade_id VARCHAR(14) PRIMARY KEY NOT NULL, nutrition_grade_desc TEXT NOT NULL);")
    cursor.execute("CREATE TABLE IF NOT EXISTS store (store_id TEXT PRIMARY KEY NOT NULL, store_desc_fr TEXT NOT NULL);")
    conn.commit()
    cursor.close()
    conn.close()


def select_categories(data):
    """
    Selects fr category id's and apply some filters
    """
    all_categories = []

    for each in data['products']:
        category = each['categories_tags']
        all_categories.append(category)

    #print(all_categories)

    all_french_categories = []

    for each in all_categories:
        for elem in each:
            if 'fr:' in elem:
                all_french_categories.append(elem)

    print(all_french_categories)


def remove_duplicates():
    pass


def import_categories():
    pass


def import_stores():
    pass


def import_products():
    pass



def main():

    if os.path.isfile('json_openfoodfacts_db.json') != True:
        get_api_data()
    else:
        read_from_local_json_file()

    create_database()
    create_table()


if __name__ == "__main__":
    main()