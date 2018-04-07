#! /usr/bin/env python3
# coding: utf-8

import psycopg2

conn = psycopg2.connect("dbname=openfoodfacts user=postgres password=postgres")
cursor = conn.cursor()


def create_category_table():
    cursor.execute("CREATE TABLE IF NOT EXISTS category (id INTEGER PRIMARY KEY, category TEXT, datestamp TEXT);")


def data_entry():
    cursor.execute("INSERT INTO category VALUES (0, 'I am a category', '2018-04-05');")
    conn.commit()
    cursor.close()
    conn.close()


def read_from_db():
    cursor.execute("SELECT * FROM category")
    # data = cursor.fetchall()
    for row in cursor.fetchall():
        print(row)


# create_category_table()
# data_entry()

read_from_db()
