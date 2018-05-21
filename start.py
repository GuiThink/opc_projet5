#! /usr/bin/env python3
# coding: utf-8

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_database():

    conn = psycopg2.connect(host="localhost", user="postgres", password="postgres")
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE openfoodfacts_db ENCODING 'UTF8';")
    conn.commit()
    cursor.close()
    conn.close()


def create_table():

    conn = psycopg2.connect(host="localhost", database="openfoodfacts_db", user="postgres", password="postgres")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS category (id SERIAL PRIMARY KEY, category_id TEXT NOT NULL, category_name_fr TEXT NOT NULL);")
    cursor.execute("CREATE TABLE IF NOT EXISTS product (product_id VARCHAR(100) PRIMARY KEY NOT NULL, category_id VARCHAR(100) NOT NULL, product_name_fr VARCHAR(100) NOT NULL, nutrition_grade_id VARCHAR(14) NOT NULL, product_url_fr TEXT NOT NULL);")
    cursor.execute("CREATE TABLE IF NOT EXISTS nutrition_grade (nutrition_grade_id VARCHAR(14) PRIMARY KEY NOT NULL, nutrition_grade_desc TEXT NOT NULL);")
    cursor.execute("CREATE TABLE IF NOT EXISTS store (store_id TEXT PRIMARY KEY NOT NULL, store_desc_fr TEXT NOT NULL);")
    conn.commit()
    cursor.close()
    conn.close()

create_database()
create_table()
