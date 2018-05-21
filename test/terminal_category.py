#! /usr/bin/env python3
# coding: utf-8
import requests
import psycopg2


conn = psycopg2.connect(host="localhost", database="openfoodfacts_db", user="postgres", password="postgres")
cursor = conn.cursor()


def read_from_category_table():
    cursor.execute("SELECT id, category_name_fr FROM category LIMIT 50")

    datas = cursor.fetchall()
    for index, elem in datas:
        print(f"{index} - {elem}")
    # print(datas[3])

    usr_input = int(input("> category : ")) -1
    print(f"Chosen category is : {datas[usr_input]}")





# def print_categories():
#
#     print('\nCategories :\n')
#     for keys, values in category_list.items():
#         print(keys, values)
#     print('\n***********\n')
#     get_category_user_input()
#
#
# def get_category_user_input():
#
#     while True:
#        try:
#            category_user_input = input('> Please, type the number of the chosen category and press ENTER :')
#        except ValueError:
#            print('That\'s not a number!')
#        else:
#            if str(1) <= category_user_input <= str(3): # problème : trouver comment se baser sur la longueur de la liste
#                break
#            else:
#                print('Out of range. You need to type a category number corresponding to the category list.')
#     print(f'\nYou have chosen the following category : {category_list[category_user_input]}')
#     print_products(category_user_input)
#
#
# def print_products(category_user_input):
#
#     print(f'\nProducts related to : {category_list[category_user_input]}\n')
#     for keys, values in product_list[category_user_input].items():
#         print(keys, values)
#     print('\n***********\n')
#     get_product_user_input(category_user_input)
#
#
# def get_product_user_input(category_user_input):
#
#     while True:
#        try:
#            product_user_input = input('> Please, type the number of the chosen product and press ENTER :')
#        except ValueError:
#            print('That\'s not a number!')
#        else:
#            if str(1) <= product_user_input <= str(4): # problème : trouver comment se baser sur la longueur de la liste
#                break
#            else:
#                print('Out of range. You need to type a product number corresponding to the product list.')
#     print(f'\nYou have chosen the following product : {product_list[category_user_input][product_user_input]}')


def main():
    # print_categories()
    read_from_category_table()

if __name__ == "__main__":
    main()
