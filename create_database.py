#! /usr/bin/env python3
# coding: utf-8

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

conn = psycopg2.connect(host="localhost", user="postgres", password="postgres")
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor = conn.cursor()

def create_database():
    cursor.execute("CREATE DATABASE a_database_from_python;")
    # conn.commit()
    cursor.close()
    conn.close()


create_database()
