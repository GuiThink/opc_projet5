#! /usr/bin/env python3
# coding: utf-8

import psycopg2

conn = psycopg2.connect(host="localhost", database="openfoodfacts_db", user="postgres", password="postgres")
cursor = conn.cursor()


def create_category_table():
    cursor.execute("CREATE TABLE IF NOT EXISTS category (id SERIAL PRIMARY KEY, category_id TEXT NOT NULL, category_name_fr TEXT NOT NULL);")


def create_product_table():
    cursor.execute("CREATE TABLE IF NOT EXISTS product (product_id VARCHAR(100) PRIMARY KEY NOT NULL, category_id VARCHAR(100) NOT NULL, product_name_fr VARCHAR(100) NOT NULL, nutrition_grade_id VARCHAR(14) NOT NULL, product_url_fr TEXT NOT NULL);")


def create_nutrition_grade_table():
    cursor.execute("CREATE TABLE IF NOT EXISTS nutrition_grade (nutrition_grade_id VARCHAR(14) PRIMARY KEY NOT NULL, nutrition_grade_desc TEXT NOT NULL);")


def create_store_table():
    cursor.execute("CREATE TABLE IF NOT EXISTS store (store_id TEXT PRIMARY KEY NOT NULL, store_desc_fr TEXT NOT NULL);")


create_category_table()
create_product_table()
create_nutrition_grade_table()
create_store_table()

conn.commit()
cursor.close()
conn.close()
