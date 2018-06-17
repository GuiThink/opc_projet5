#! /usr/bin/env python3
# coding: utf-8

import database_creator
import nutrition_grade_mapping
import printers
import readers
import substitute
import user_inputs


def main():
    database_creator.DatabaseCreator()

    while True:
        # menu system
        menu_choice = user_inputs.main_menu()

        if menu_choice == 1:

            # read from category table
            cat_table = readers.read_category_table()
            printers.print_cat_table(cat_table)

            # get category input from user
            cat_desc = user_inputs.get_cat_input(cat_table)

            # get products related to the chosen category
            chosen_cat_related_product_list = readers.get_products_for_given_category(cat_desc)
            printers.print_products(chosen_cat_related_product_list)

            # get chosen product input from user
            pdct_input = user_inputs.get_product_input(chosen_cat_related_product_list)
            pdct_id = pdct_input[0]
            pdct_nutrition_grade = pdct_input[1]

            # find all possible substitutes to the chosen product
            potential_pdcts = readers.potential_substitute(cat_desc)

            # transform letter based nutrition grade into integer based grade
            modified_potential_pdcts_list = nutrition_grade_mapping.map_nutrition_grade_list(potential_pdcts)
            chosen_product_nutrition_grade = nutrition_grade_mapping.map_nutrition_grade(pdct_nutrition_grade)

            # find a suitable substitute among all potential possibilities
            chosen_product_id = substitute.find_substitute(pdct_id, chosen_product_nutrition_grade, modified_potential_pdcts_list)

            # show substitute details
            substitutes = readers.get_substitute_product_details(chosen_product_id)

            for pdct_attribute in substitutes:
                print("|||||||||||||| SUBSTITUTE ||||||||||||||")
                print(f">> Substitute product advised : {pdct_attribute[1]} "
                      f"\n>> Nutritional grade : {pdct_attribute[2]} "
                      f"\n>> URL : {pdct_attribute[3]}  "
                      f"\n>> Where to buy : {pdct_attribute[4]}")
                print("||||||||||||||||||||||||||||||||||||||||\n")

            # ask to save
            choice = user_inputs.yes_or_no(">> Do you want to save this ? Type YES or NO and then press ENTER : \n")

            if choice == "yes":
                substitute.save_substitute(chosen_product_id[0], pdct_id)
                print("\n>> Product saved.")
                user_inputs.menu_or_exit("\n>> Type M to go back to main menu, "
                             "or Q to leave the application, and the press ENTER : \n")
            else:
                print("\n>> Unsaved.")
                user_inputs.menu_or_exit("\n>> Type M to go back to main menu, "
                             "or type Q to leave the application, and the press ENTER : \n")
        else:
            query1 = readers.read_history_table()
            query2 = readers.read_history_table_2()
            printers.print_history(query1, query2)
            user_inputs.menu_or_exit("\n>> Type M to go back to main menu, "
                         "or type Q to leave the application, and the press ENTER : \n")


if __name__ == "__main__":
    main()
