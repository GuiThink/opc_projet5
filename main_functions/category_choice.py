#! /usr/bin/env python3
# coding: utf-8

from data_base.database_connect import UseDatabase


class CategoryChoice(object):
    """
    Generates a Category object
    """
    def __init__(self):
        self.category_list = self.get_all_categories()
        self.print_all_categories(self.category_list)
        self.category_choice = self.get_user_category_choice(self.category_list)

    def get_all_categories(self):
        """Returns all categories"""
        with UseDatabase() as cursor:
            cursor.execute("SELECT * "
                           "FROM category LIMIT 30")
            data = cursor.fetchall()

        return data

    def print_all_categories(self, category_list):
        """
        Prints out category table (cf. LIMIT)
        """
        line_id = 1

        for line in category_list:
            print(f"{line_id} | {line[0]}")
            line_id += 1

    def get_user_category_choice(self, category_list):
        """
        Get category choice from user input and returns category id
        """
        user_choice = 0
        category_list_size = len(category_list)

        while True:
            try:
                while (user_choice < 1) or (user_choice > category_list_size):
                    user_choice = int(input("\n>> Please chose a category and press ENTER : \n"))
                break
            except ValueError:
                print(">> Please, type in a number.")

        category_id = user_choice - 1
        category_choice = category_list[category_id]

        print(f"\n>> You have selected category {user_choice} | {category_list[category_id][0]} \n")

        return category_choice

