#! /usr/bin/env python3
# coding: utf-8

import psycopg2

conn = psycopg2.connect(host="localhost", database="openfoodfacts_db", user="postgres", password="postgres")
cursor = conn.cursor()


def create_category_table():
    cursor.execute("CREATE TABLE IF NOT EXISTS category (category_id VARCHAR(100)PRIMARY KEY NOT NULL, category_name_fr VARCHAR(100) NOT NULL);")


def create_product_table():
    cursor.execute("CREATE TABLE IF NOT EXISTS product (product_id VARCHAR(100) PRIMARY KEY NOT NULL, category_id VARCHAR(100) NOT NULL, product_name_fr VARCHAR(100) NOT NULL, nutrition_grade_id VARCHAR(14) NOT NULL, product_url_fr TEXT NOT NULL);")


def create_nutrition_grade_table():
    cursor.execute("CREATE TABLE IF NOT EXISTS nutrition_grade (nutrition_grade_id VARCHAR(14) PRIMARY KEY NOT NULL, nutrition_grade_desc TEXT NOT NULL);")


def create_store_table():
    cursor.execute("CREATE TABLE IF NOT EXISTS store (store_id TEXT PRIMARY KEY NOT NULL, store_desc_fr TEXT NOT NULL);")



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
