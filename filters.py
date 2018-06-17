#! /usr/bin/env python3
# coding: utf-8


def filter_categories(raw_data):
    """
    Selects fr category id's and apply some filters
    """
    raw_categories = []

    for product in raw_data['products']:
        category_list = product['categories_tags']
        raw_categories += category_list

    fr_categories = []

    for category in raw_categories:
        if 'fr:' in category:
            fr_categories.append(category)

    keepers = []
    occurrence_limit = 2

    for category in fr_categories:
        if fr_categories.count(category) >= occurrence_limit:
            keepers.append(category)

    return keepers


def filter_products(raw_data, keepers):
    """
    Uses the raw json file and the list of category keepers (categories with at least 2 or more products)
    to find the products that correspond to these categories and then appends these products details to a product list
    """
    raw_product_list = []

    for product in raw_data['products']:
        category_list = product['categories_tags']

        for cat in category_list:

            if cat in keepers:
                try:
                    product_id = product['id']
                    product_name_fr = product['product_name_fr']
                    product_nutrition_grade = product['nutrition_grades']
                    product_url_fr = product['url']
                    product_store = product['stores_tags'][0]  # takes the first store found

                    raw_product_list.append((product_id, product_name_fr, product_nutrition_grade,
                                             product_url_fr, product_store, cat))
                except (KeyError, IndexError):
                    continue

            else:
                continue

    clean_product_list = []
    check_list = set()

    for elem in raw_product_list:
        product_name = elem[1]
        if product_name not in check_list:
            clean_product_list.append(elem)
            check_list.add(product_name)

    return clean_product_list


def filter_stores(raw_data, keepers):
    """
    Creates a list of stores that contains all stores found for each category present in category keepers list
    """
    store_list = []
    for product in raw_data['products']:
        category_list = product['categories_tags']
        # print(category_list)
        for cat in category_list:
            try:
                if cat in keepers:
                    product_store = product['stores_tags']
                    if product_store:
                        store_list.append(product_store)
                    else:
                        continue
                else:
                    continue
            except KeyError:
                pass

    store_keepers = []

    for elem in store_list:
        store_keepers += elem

    return store_keepers


def remove_duplicates(list_to_clean):
    """
    Removes duplicates from a given list
    """
    return set(list_to_clean)
