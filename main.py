#! /usr/bin/env python3
# coding: utf-8

from database_connect import UseDatabase
from datetime import datetime
from create_database import *
from insert_into_database import *
from api_json import *


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


def remove_duplicates(list_to_clean):
    """
    Removes duplicates from a given list
    """
    return set(list_to_clean)


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


def print_products(product_list):
    """
    Prints out the products in the terminal with an index so user can later type a number
    to chose the products he desires to find a substitute for.
    """
    pdct_id = 1
    for pdct in product_list:
        print(f"{pdct_id} | {pdct[1]}")
        pdct_id += 1


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


def map_nutrition_grade(nutrition_grade):
    """
    Process of mapping the letter-based nutrition grades with numerical-based nutrition
    grades so they can be compared easier. Apply this to the product nutrition grade that the user chose
    in the Terminal.
    """
    nutrition_grade_dict = {'a': 5, 'b': 5, 'c': 3, 'd': 2, 'e': 1, 'f': 0}

    for grade in nutrition_grade_dict:
        if nutrition_grade == grade:
            nutrition_grade = nutrition_grade_dict[grade]
        else:
            pass

    return nutrition_grade


def map_nutrition_grade_list(potential_pdcts):
    """
    Process of mapping the letter-based nutrition grades with numerical-based nutrition
    grades so they can be compared easier. Apply this to the list of potential substitutes
    """
    nutrition_grade_dict = {'a': 5, 'b': 5, 'c': 3, 'd': 2, 'e': 1, 'f': 0}

    modified_potential_pdcts_list = []

    for each in potential_pdcts:
        product_id = each[0]
        product_name = each[1]
        product_nutrition_grade = each[2]
        product_url = each[3]
        product_shop = each[4]
        product_category = each[5]

        if product_nutrition_grade in nutrition_grade_dict:
            grade = nutrition_grade_dict[product_nutrition_grade]
            modified_potential_pdcts_list.append((product_id, product_name,
                                                  grade, product_url, product_shop, product_category))

    return modified_potential_pdcts_list


def save_substitute(chosen_product_id):
    """
    Process of saving the current substitute product into the history table
    """
    dt = datetime.now()

    with UseDatabase() as cursor:
        cursor.execute("INSERT INTO history (product_id, date_time) VALUES (%s, %s)", (chosen_product_id, dt,))


def read_history_table():
    """
    Prints out the last 10 products saved by user
    """
    with UseDatabase() as cursor:
        cursor.execute("""SELECT product.product_id, product.product_name_fr,
                          product.product_nutrition_grade, product.product_url,
                          product.store_id, product.category_id, history.date_time
                          FROM product, category, history, store
                          WHERE product.product_id = history.product_id 
                          AND product.store_id = store.store_id 
                          AND product.category_id = category.category_id
                          ORDER BY history.date_time ASC
                          LIMIT 10""")
        data = cursor.fetchall()

    print("\n>> Your saved products : \n")

    for elem in data:
        print(f"{elem[6]} \n\t{elem[0]} \n\t{elem[1]} \n\t{elem[5]} \n\t{elem[3]} \n\t{elem[4]} \n\t{elem[2]}\n")

    return data


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
            continue

    return chosen_product_id


def print_cat_table(cat_table):
    """
    Prints out category table (cf. LIMIT)
    """
    cat_id = 1

    for category in cat_table:
        print(f"{cat_id} | {category[0]}")
        cat_id += 1


def get_cat_input(cat_table):
    """
    Get category choice from user input and returns category id
    """
    cat_input = 0
    cat_list_size = len(cat_table)

    while True:
        try:
            while (cat_input < 1) or (cat_input > cat_list_size):
                cat_input = int(input("\n>> Please chose a category and press ENTER : \n"))
            break
        except ValueError:
            print(">> Please, type in a number.")

    cat_index = cat_input - 1
    cat_desc = cat_table[cat_index]

    print(f"\n>> You have selected category {cat_input} | {cat_table[cat_index][0]} \n")

    return cat_desc


def get_product_input(chosen_cat_related_product_list):
    """
    Prints out the product chosen by the user as a base for substitute research
    """
    pdct_input = 0
    pdct_list_size = len(chosen_cat_related_product_list)

    while True:
        try:
            while (pdct_input < 1) or (pdct_input > pdct_list_size):
                pdct_input = int(input("\n>> Please chose a product and press ENTER : \n"))
            break
        except ValueError:
            print(">> Please, type in a number.")

    pdct_index = pdct_input - 1
    pdct_id = chosen_cat_related_product_list[pdct_index][0]
    pdct_nutrition_grade = chosen_cat_related_product_list[pdct_index][2]

    print(f"\n>> You have selected product {pdct_input} "
          f"| {chosen_cat_related_product_list[pdct_index][1]} \n")

    return pdct_id, pdct_nutrition_grade


def main_menu():
    """
    Main menu of the application
    """
    menu_choice = 0

    print(">> Welcome !")
    print(">> What do you want to do ?\n")
    print("1 | Find a substitute")
    print("2 | Consult my substitutes history\n")

    while True:
        try:
            while (menu_choice < 1) or (menu_choice > 2):
                menu_choice = int(input(">> Type your choice and press ENTER : \n"))
            break
        except ValueError:
            print(">> Please, type in a number.")

    return menu_choice


def menu_or_exit(prompt):
    """
    Saves the saving choice of user (yes or no)
    """
    while True:
        choice = input(prompt).strip().upper()
        if choice == "M":
            main()
        elif choice == "Q":
            print("See you next time !")
            break
        else:
            continue


def yes_or_no(prompt):
    """
    Saves the saving choice of user (yes or no)
    """
    while True:
        choice = input(prompt).strip().lower()
        if choice in ("yes", "no"):
            return choice


def main():
    # database and tables creation process
    create_database()
    create_table()

    # data retrieving process
    if not os.path.isfile('json_openfoodfacts_db.json'):
        get_api_data()

    raw_data = read_from_local_json_file()

    # category filtering process
    category_keepers = filter_categories(raw_data)
    ready_to_go_category_list = sorted(remove_duplicates(category_keepers))

    # product filtering process
    ready_to_go_product_list = sorted(filter_products(raw_data, category_keepers))

    # store filtering process
    store_keepers = filter_stores(raw_data, category_keepers)
    ready_to_go_store_list = sorted(remove_duplicates(store_keepers))

    # inserts process
    insert_into_category(ready_to_go_category_list)
    insert_into_store(ready_to_go_store_list)
    insert_into_product(ready_to_go_product_list)

    # menu system
    menu_choice = main_menu()

    if menu_choice == 1:

        # read from category table
        cat_table = read_category_table()
        print_cat_table(cat_table)

        # get category input from user
        cat_desc = get_cat_input(cat_table)

        # get products related to the chosen category
        chosen_cat_related_product_list = get_products_for_given_category(cat_desc)
        print_products(chosen_cat_related_product_list)

        # get chosen product input from user
        pdct_input = get_product_input(chosen_cat_related_product_list)
        pdct_id = pdct_input[0]
        pdct_nutrition_grade = pdct_input[1]

        # find all possible substitutes to the chosen product
        potential_pdcts = potential_substitute(cat_desc)

        # transform letter based nutrition grade into integer based grade
        modified_potential_pdcts_list = map_nutrition_grade_list(potential_pdcts)
        chosen_product_nutrition_grade = map_nutrition_grade(pdct_nutrition_grade)

        # find a suitable substitute among all potential possibilities
        chosen_product_id = find_substitute(pdct_id, chosen_product_nutrition_grade, modified_potential_pdcts_list)

        # show substitute details
        substitutes = get_substitute_product_details(chosen_product_id)

        for pdct_attribute in substitutes:
            print("|||||||||||||| SUBSTITUTE ||||||||||||||")
            print(f">> Substitute product advised : {pdct_attribute[1]} "
                  f"\n>> Nutritional grade : {pdct_attribute[2]} "
                  f"\n>> URL : {pdct_attribute[3]}  "
                  f"\n>> Where to buy : {pdct_attribute[4]}")
            print("||||||||||||||||||||||||||||||||||||||||\n")

        # ask to save
        choice = yes_or_no(">> Do you want to save this ? Type YES or NO and then press ENTER : \n")

        if choice == "yes":
            save_substitute(chosen_product_id[0])
            print("\n>> Product saved.")
            menu_or_exit("\n>> Type M to go back to main menu, "
                         "or Q to leave the application, and the press ENTER : \n")
        else:
            print("\n>> Unsaved.")
            menu_or_exit("\n>> Type M to go back to main menu, "
                         "or type Q to leave the application, and the press ENTER : \n")
    else:
        read_history_table()
        menu_or_exit("\n>> Type M to go back to main menu, "
                     "or type Q to leave the application, and the press ENTER : \n")


if __name__ == "__main__":
    main()
