#! /usr/bin/env python3
# coding: utf-8

from data_base.database_creator import DatabaseCreator
from data_base.get_json_from_api import Json
from data_base.inserts import Inserts
from main_functions.category_choice import CategoryChoice
from main_functions.history import History
from main_functions.product_choice import ProductChoice
from main_functions.save import Save
from nav.menu import Menu
from processing.filters import Filters
from processing.substitute import Substitute


def main():

    DatabaseCreator()
    Json()
    raw_data = Json.read_local_json()
    filtered_datas = Filters(raw_data)
    Inserts(filtered_datas.ready_categories, filtered_datas.ready_stores, filtered_datas.ready_products)

    while True:

        menu = Menu()

        if menu.menu_choice == 1:

            categories = CategoryChoice()

            chosen_product = ProductChoice(categories.category_choice)

            subsitute = Substitute(chosen_product.category_choice, chosen_product.pdct_input, chosen_product.pdct_index,
                                   chosen_product.pdct_id, chosen_product.pdct_nutrition_grade)

            save = Save()

            if save.saving_choice == 'yes':
                save.save_substitute(subsitute.chosen_product_id[0], chosen_product.pdct_id)
                menu.back_to_menu_or_exit()
            else:
                menu.back_to_menu_or_exit()

        else:
            History()
            menu.back_to_menu_or_exit()


if __name__ == "__main__":
    main()
