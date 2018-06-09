#! /usr/bin/env python3
# coding: utf-8

import psycopg2
from database_connect import UseDatabase


def insert_into_category(ready_to_go_category_list):
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
        print(">> CATEGORY TABLE INFO : datas inserted into table.")
    except psycopg2.IntegrityError:
        print(">> CATEGORY TABLE INFO : PK already exists into table. Ignoring new insert.")
        pass


def insert_into_store(ready_to_go_store_list):
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
        print(">> STORE TABLE INFO : datas inserted into table.")
    except psycopg2.IntegrityError:
        print(">> STORE TABLE INFO : PK already exists into table. Ignoring new insert.")
        pass


def insert_into_product(ready_to_go_product_list):
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
        print(">> PRODUCT TABLE INFO : datas inserted into table.")
    except psycopg2.IntegrityError:
        print(">> PRODUCT TABLE INFO : PK already exists into table. Ignoring new insert.")
        pass

