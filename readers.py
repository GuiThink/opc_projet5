#! /usr/bin/env python3
# coding: utf-8
from database_connect import UseDatabase


def read_category_table():
    """
    Returns a list with all categories* (*cf. LIMIT)
    """
    with UseDatabase() as cursor:
        cursor.execute("SELECT category_id FROM category LIMIT 30")
        data = cursor.fetchall()

    return data


def read_store_table():
    """
    Returns a lost with all stores
    """
    with UseDatabase() as cursor:
        cursor.execute("SELECT store_id FROM store")
        data = cursor.fetchall()

    return data


def read_history_table():
    """
    Prints out the last 10 products saved by user
    """
    with UseDatabase() as cursor:
        cursor.execute("""SELECT product.product_id, product.product_name_fr,
                          product.product_nutrition_grade, product.product_url,
                          product.store_id, product.category_id, history.date_time,
                          history.initial_product_id
                          FROM product, category, history, store
                          WHERE product.product_id = history.product_id
                          AND product.store_id = store.store_id
                          AND product.category_id = category.category_id
                          ORDER BY history.date_time ASC
                          LIMIT 10""")

        data = cursor.fetchall()

    return data


def read_history_table_2():
    """
    Prints out the last 10 initial products saved by user
    """
    with UseDatabase() as cursor:
        cursor.execute("""SELECT product.product_name_fr, product.product_nutrition_grade
                          FROM product, history
                          WHERE product.product_id = history.initial_product_id
                          ORDER BY history.date_time ASC
                          LIMIT 10""")

        data = cursor.fetchall()

    return data


def get_products_for_given_category(cat_desc):
    """
    Returns a list with all the details of all products found in the database and that have the specified category_id.
    """
    with UseDatabase() as cursor:
        cursor.execute(
            "SELECT product.product_id, product.product_name_fr, "
            "product.product_nutrition_grade "
            "FROM product, category "
            "WHERE product.category_id = category.category_id "
            "AND category.category_id = %s",
            cat_desc)
        data = cursor.fetchall()

    return data


def potential_substitute(cat_desc):
    """
    Returns a list of potential substitutes to work with. These substitutes are chosen
    depending on the category that was chosen by the user in the Terminal.
    """

    with UseDatabase() as cursor:
        cursor.execute("SELECT * FROM product WHERE category_id = %s", cat_desc)
        data = cursor.fetchall()

    return data


def get_chosen_product_details(pdct_id):
    """
    Gets the details of the product that was chosen by the user in the Terminal.
    """
    data_to_insert = list(pdct_id.split())

    with UseDatabase() as cursor:
        cursor.execute("SELECT * FROM product WHERE product_id = %s", data_to_insert)
        data = cursor.fetchall()

    return data


def get_substitute_product_details(chosen_pdct_id):
    """
    Shows the details of the substitute product
    """
    with UseDatabase() as cursor:
        cursor.execute("SELECT * FROM product WHERE product_id = %s", chosen_pdct_id)
        data = cursor.fetchall()

    return data
