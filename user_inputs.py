#! /usr/bin/env python3
# coding: utf-8


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
            break
        elif choice == "Q":
            print("See you next time !")
            exit()
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


