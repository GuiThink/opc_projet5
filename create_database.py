#! /usr/bin/env python3
# coding: utf-8

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from database_connect import UseDatabase


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
    with UseDatabase() as cursor:
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS category (category_id VARCHAR(255) UNIQUE NOT NULL, PRIMARY KEY(category_id));")

        cursor.execute("CREATE TABLE IF NOT EXISTS store (store_id VARCHAR(255) UNIQUE NOT NULL, PRIMARY KEY (store_id));")

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
                          date_time TIMESTAMP NOT NULL);""")

