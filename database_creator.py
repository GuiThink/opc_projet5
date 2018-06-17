#! /usr/bin/env python3
# coding: utf-8
import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from database_connect import UseDatabase
from api_json import get_api_data, read_from_local_json_file
from filters import filter_categories, remove_duplicates, filter_products, filter_stores


class DatabaseCreator:
    def __init__(self):
        # database and tables creation process
        self.create_database()
        self.create_table()

        # data retrieving process
        if not os.path.isfile('json_openfoodfacts_db.json'):
            get_api_data()
        self.raw_data = read_from_local_json_file()

        # category filtering process
        self.category_keepers = filter_categories(self.raw_data)
        self.ready_to_go_category_list = sorted(remove_duplicates(self.category_keepers))

        # product filtering process
        self.ready_to_go_product_list = sorted(filter_products(self.raw_data, self.category_keepers))

        # store filtering process
        self.store_keepers = filter_stores(self.raw_data, self.category_keepers)
        self.ready_to_go_store_list = sorted(remove_duplicates(self.store_keepers))

        # inserts process
        self.insert_into_category(self.ready_to_go_category_list)
        self.insert_into_store(self.ready_to_go_store_list)
        self.insert_into_product(self.ready_to_go_product_list)

    def create_database(self):
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

    def create_table(self):
        """
        Tables creation process
        """
        with UseDatabase() as cursor:
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS category (category_id VARCHAR(255) UNIQUE NOT NULL, "
                "PRIMARY KEY(category_id));")

            cursor.execute(
                "CREATE TABLE IF NOT EXISTS store (store_id VARCHAR(255) UNIQUE NOT NULL, PRIMARY KEY (store_id));")

            cursor.execute("""CREATE TABLE IF NOT EXISTS product 
                              (product_id VARCHAR(255) UNIQUE NOT NULL,
                              product_name_fr VARCHAR(255) NOT NULL,
                              product_nutrition_grade VARCHAR(1) NOT NULL,
                              product_url VARCHAR(255) NOT NULL,
                              store_id VARCHAR(255) NOT NULL REFERENCES store (store_id),
                              category_id VARCHAR(255) NOT NULL REFERENCES category (category_id),
                              PRIMARY KEY (product_id)
                              );""")

            cursor.execute("""CREATE TABLE IF NOT EXISTS history 
                              (product_id VARCHAR(255) NOT NULL REFERENCES product (product_id),
                              initial_product_id VARCHAR(255) NOT NULL REFERENCES product (product_id),
                              date_time TIMESTAMP NOT NULL);""")

    def insert_into_category(self, ready_to_go_category_list):
        """
        Inserts selected categories into category table
        """
        data_to_insert = []

        for elem in ready_to_go_category_list:
            split_elem = list(elem.split())
            data_to_insert.append(split_elem)

        try:
            with UseDatabase() as cursor:
                for each in data_to_insert:
                    cursor.execute("INSERT INTO category (category_id) VALUES (%s)", each)
        except psycopg2.IntegrityError:
            pass

    def insert_into_store(self, ready_to_go_store_list):
        """
        Inserts store list into store table
        """
        data_to_insert = []

        for elem in ready_to_go_store_list:
            split_elem = list(elem.split())
            data_to_insert.append(split_elem)

        try:
            with UseDatabase() as cursor:
                for each in data_to_insert:
                    cursor.execute("INSERT INTO store (store_id) VALUES (%s)", each)
        except psycopg2.IntegrityError:
            pass

    def insert_into_product(self, ready_to_go_product_list):
        """
        Inserts products into product table
        """
        try:
            with UseDatabase() as cursor:
                for each in ready_to_go_product_list:
                    cursor.execute("""INSERT INTO product 
                                      (product_id, product_name_fr, product_nutrition_grade, 
                                      product_url, store_id, category_id) 
                                      VALUES (%s, %s, %s, %s, %s, %s)""", each)
        except psycopg2.IntegrityError:
            pass
