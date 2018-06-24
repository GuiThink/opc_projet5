#! /usr/bin/env python3
# coding: utf-8

from data_base.database_connect import UseDatabase


class ProductChoice(object):
    """
    Generates a Product object
    """
    def __init__(self, category_choice):
        self.category_choice = category_choice
        self.product_list = self.get_products_for_given_category(self.category_choice)
        self.print_products(self.product_list)
        self.pdct_input = self.get_pdct_input(self.product_list)
        self.pdct_index = self.get_pdct_index(self.pdct_input)
        self.pdct_id = self.get_pdct_id(self.product_list, self.pdct_index)
        self.pdct_nutrition_grade = self.get_pdct_nutrition_grade(self.product_list, self.pdct_index)
        self.print_selected_product(self.product_list, self.pdct_input, self.pdct_index)

    def get_products_for_given_category(self, category):
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
                category)
            product_list = cursor.fetchall()

        return product_list

    def print_products(self, product_list):
        """
        Prints out the products in the terminal with an index so user can later type a number
        to chose the products he desires to find a substitute for.
        """
        pdct_id = 1
        for pdct in product_list:
            print(f"{pdct_id} | {pdct[1]}")
            pdct_id += 1

    def get_pdct_input(self, product_list):
        """
        Prints out the product chosen by the user as a base for substitute research
        """
        pdct_input = 0
        pdct_list_size = len(product_list)

        while True:
            try:
                while (pdct_input < 1) or (pdct_input > pdct_list_size):
                    pdct_input = int(input("\n>> Please chose a product and press ENTER : \n"))
                break
            except ValueError:
                print(">> Please, type in a number.")

        return pdct_input

    def get_pdct_index(self, pdct_input):
        """
        Get the product index for the chosen product
        """
        pdct_index = pdct_input - 1

        return pdct_index

    def get_pdct_id(self, product_list, pdct_index):
        """
        Get the product id for the chosen product
        """
        pdct_id = product_list[pdct_index][0]

        return pdct_id

    def get_pdct_nutrition_grade(self, product_list, pdct_index):
        """
        Get the product nutrition grade for the chosen product
        """
        pdct_nutrition_grade = product_list[pdct_index][2]

        return pdct_nutrition_grade

    def print_selected_product(self, product_list, pdct_input, pdct_index):
        """
        Prints the selected product
        """
        print(f"\n>> You have selected product {pdct_input} "
              f"| {product_list[pdct_index][1]} \n")

