#! /usr/bin/env python3
# coding: utf-8
from datetime import datetime
from database_connect import UseDatabase


def find_substitute(pdct_id, chosen_product_nutrition_grade, modified_potential_pdcts_list):
    """
    Process of finding the first better alternative (with better or equal nutrition grade)
    """
    chosen_product_id = []
    product_count = 1

    for product in modified_potential_pdcts_list:
        if product[0] != pdct_id and product[2] >= chosen_product_nutrition_grade:
            if product_count == 1:
                chosen_product_id.append(product[0])
                product_count -= 1
            else:
                pass
        else:
            if product[0] == pdct_id and product_count == 1:
                chosen_product_id.append(product[0])
                product_count -= 1
                print(">> No better product found than the one you chose. "
                      "\nFollowing substitute advise will be the same product.")

    return chosen_product_id


def save_substitute(chosen_product_id, initial_product_id):
    """
    Process of saving the current substitute product into the history table
    """
    dt = datetime.now()

    with UseDatabase() as cursor:
        cursor.execute("INSERT INTO history (product_id, initial_product_id, date_time) "
                       "VALUES (%s, %s, %s)", (chosen_product_id, initial_product_id, dt))
