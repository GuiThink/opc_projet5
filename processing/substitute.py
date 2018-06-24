#! /usr/bin/env python3
# coding: utf-8

from data_base.database_connect import UseDatabase


class Substitute(object):
    """
    Class to find and work with substitutes
    """
    def __init__(self, category_choice, pdct_input, pdct_index, pdct_id, pdct_nutrition_grade):
        self.category_choice = category_choice
        self.pdct_input = pdct_input
        self.pdct_index = pdct_index
        self.pdct_id = pdct_id
        self.pdct_nutrition_grade = pdct_nutrition_grade
        self.potential_substitutes = self.potential_substitutes(self.category_choice)
        self.modified_potential_pdcts_list = self.map_nutrition_grade_list(self.potential_substitutes)
        self.modified_pdct_nutrition_grade = self.map_nutrition_grade(self.pdct_nutrition_grade)
        self.chosen_product_id = self.find_substitute(self.pdct_id, self.modified_pdct_nutrition_grade, self.modified_potential_pdcts_list)
        self.get_substitute_product_details(self.chosen_product_id)

    def potential_substitutes(self, category_choice):
        """
        Returns a list of potential substitutes to work with. These substitutes are chosen
        depending on the category that was chosen by the user in the Terminal.
        """
        with UseDatabase() as cursor:
            cursor.execute("SELECT * FROM product WHERE category_id = %s", category_choice)
            potential_substitutes = cursor.fetchall()

        return potential_substitutes

    def map_nutrition_grade_list(self, potential_substitutes):
        """
        Process of mapping the letter-based nutrition grades with numerical-based nutrition
        grades so they can be compared easier. Apply this to the list of potential substitutes
        """
        nutrition_grade_dict = {'a': 5, 'b': 5, 'c': 3, 'd': 2, 'e': 1, 'f': 0}

        modified_potential_pdcts_list = []

        for each in potential_substitutes:
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

    def map_nutrition_grade(self, pdct_nutrition_grade):
        """
        Process of mapping the letter-based nutrition grades with numerical-based nutrition
        grades so they can be compared easier. Apply this to the product nutrition grade that the user chose
        in the Terminal.
        """
        nutrition_grade_dict = {'a': 5, 'b': 5, 'c': 3, 'd': 2, 'e': 1, 'f': 0}
        modified_pdct_nutrition_grade = 0

        for grade in nutrition_grade_dict:
            if pdct_nutrition_grade == grade:
                modified_pdct_nutrition_grade = nutrition_grade_dict[grade]
            else:
                pass

        return modified_pdct_nutrition_grade

    def find_substitute(self, pdct_id, modified_pdct_nutrition_grade, modified_potential_pdcts_list):
        """
        Process of finding the first better alternative (with better or equal nutrition grade)
        """

        chosen_product_id = []
        initial_product_id = []
        product_count = 1

        for product in modified_potential_pdcts_list:
            if product[0] == pdct_id:
                initial_product_id.append(product[0])
            else:
                if product[0] != pdct_id and product[2] >= modified_pdct_nutrition_grade:
                    if product_count == 1:
                        chosen_product_id.append(product[0])
                        product_count -= 1
                else:
                    continue

        if product_count == 0:
            return chosen_product_id
        else:
            chosen_product_id = initial_product_id
            print(">> No better product found than the one you chose. "
                  "\nFollowing substitute advise will be the same product.")
            return chosen_product_id


    def get_substitute_product_details(self, chosen_pdct_id):
        """
        Shows the details of the substitute product
        """
        print(chosen_pdct_id)
        with UseDatabase() as cursor:
            cursor.execute("SELECT * FROM product WHERE product_id = %s", chosen_pdct_id)
            data = cursor.fetchall()

        for pdct_attribute in data:
            print("|||||||||||||| SUBSTITUTE ||||||||||||||")
            print(f">> Substitute product advised : {pdct_attribute[1]} "
                  f"\n>> Nutritional grade : {pdct_attribute[2]} "
                  f"\n>> URL : {pdct_attribute[3]}  "
                  f"\n>> Where to buy : {pdct_attribute[4]}")
            print("||||||||||||||||||||||||||||||||||||||||\n")
