#! /usr/bin/env python3
# coding: utf-8

import psycopg2

conn = psycopg2.connect(host="localhost", database="openfoodfacts_db", user="postgres", password="postgres")
cursor = conn.cursor()


def create_category_table():
    cursor.execute("CREATE TABLE IF NOT EXISTS category (category_id TEXT PRIMARY KEY, category_name_fr TEXT, datestamp TEXT);")


def create_product_table():
    cursor.execute("CREATE TABLE IF NOT EXISTS product (product_id INTEGER PRIMARY KEY, category_id INTEGER, product_name_fr TEXT, nutrition_grade_id INTEGER, product_url_fr TEXT, datestamp TEXT);")


def create_nutrition_grade_table():
    cursor.execute("CREATE TABLE IF NOT EXISTS nutrition_grade (nutrition_grade_id INTEGER PRIMARY KEY, nutrition_grade_desc TEXT, datestamp TEXT);")


def create_store_table():
    cursor.execute("CREATE TABLE IF NOT EXISTS store (store_id INTEGER PRIMARY KEY, store_desc_fr TEXT, datestamp TEXT);")



# def data_entry():
#     cursor.execute("INSERT INTO category VALUES (0, 'I am a category', '2018-04-05');")
#     conn.commit()
#     cursor.close()
#     conn.close()


# def read_from_db():
#     cursor.execute("SELECT * FROM category")
#     # data = cursor.fetchall()
#     for row in cursor.fetchall():
#         print(row)


# create_category_table()
# data_entry()

create_category_table()
create_product_table()
create_nutrition_grade_table()
create_store_table()


conn.commit()
cursor.close()
conn.close()
