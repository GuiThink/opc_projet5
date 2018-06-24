#! /usr/bin/env python3
# coding: utf-8

import psycopg2


class UseDatabase:
    """
    Database connection class
    """

    def __init__(self) -> None:
        dbconfig = {
            "host": "localhost",
            "database": "openfoodfacts_db",
            "user": "postgres",
            "password": "postgres",
            }
        self.configuration = dbconfig
        self.conn = psycopg2.connect(**self.configuration)
        self.cursor = self.conn.cursor()

    def __enter__(self):
        return self.cursor

    def __exit__(self, exc_type, exc_value, exc_trace) -> None:
        self.conn.commit()

    def __del__(self):
        self.cursor.close()
        self.conn.close()
