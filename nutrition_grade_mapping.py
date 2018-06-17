#! /usr/bin/env python3
# coding: utf-8


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
