#! /usr/bin/env python3
# coding: utf-8

import psycopg2
from data_base.database_connect import UseDatabase


class Inserts(object):
    """
    Manages all inserts into Database tables
    """
    def __init__(self, ready_categories, ready_stores, ready_products):
        self.ready_categories = ready_categories
        self.ready_stores = ready_stores
        self.ready_products = ready_products
        self.insert_into_category(self.ready_categories)
        self.insert_into_store(self.ready_stores)
        self.insert_into_product(self.ready_products)

    def insert_into_category(self, ready_categories):
        """
        Inserts selected categories into category table
        """
        data_to_insert = []

        for elem in ready_categories:
            split_elem = list(elem.split())
            data_to_insert.append(split_elem)

        try:
            with UseDatabase() as cursor:
                for each in data_to_insert:
                    cursor.execute("INSERT INTO category (category_id) VALUES (%s)", each)
        except psycopg2.IntegrityError:
            pass

    def insert_into_store(self, ready_stores):
        """
        Inserts store list into store table
        """
        data_to_insert = []

        for elem in ready_stores:
            split_elem = list(elem.split())
            data_to_insert.append(split_elem)

        try:
            with UseDatabase() as cursor:
                for each in data_to_insert:
                    cursor.execute("INSERT INTO store (store_id) VALUES (%s)", each)
        except psycopg2.IntegrityError:
            pass

    def insert_into_product(self, ready_products):
        """
        Inserts products into product table
        """
        try:
            with UseDatabase() as cursor:
                for each in ready_products:
                    cursor.execute("""INSERT INTO product 
                                      (product_id, product_name_fr, product_nutrition_grade, 
                                      product_url, store_id, category_id) 
                                      VALUES (%s, %s, %s, %s, %s, %s)""", each)
        except psycopg2.IntegrityError:
            pass