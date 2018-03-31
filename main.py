#! /usr/bin/env python3
# coding: utf-8

category_list = {'1':'pain','2':'viande','3':'poisson'}
product_list = {'1':{'1':'brioche','2':'baguette','3':'pain de campagne'},'2':{'1':'boeuf','2':'poulet'},'3':{'1':'morue','2':'truite','3':'requin','4':'bulot'}}


def print_categories():

    print('\nCategories :\n')
    for keys, values in category_list.items():
        print(keys, values)
    print('\n***********\n')
    get_category_user_input()


def get_category_user_input():

    while True:
       try:
           category_user_input = input('> Please, type the number of the chosen category and press ENTER :')
       except ValueError:
           print('That\'s not a number!')
       else:
           if str(1) <= category_user_input <= str(3): # problème : trouver comment se baser sur la longueur de la liste
               break
           else:
               print('Out of range. You need to type a category number corresponding to the category list.')
    print(f'\nYou have chosen the following category : {category_list[category_user_input]}')
    print_products(category_user_input)


def print_products(category_user_input):

    print(f'\nProducts related to : {category_list[category_user_input]}\n')
    for keys, values in product_list[category_user_input].items():
        print(keys, values)
    print('\n***********\n')
    get_product_user_input(category_user_input)


def get_product_user_input(category_user_input):

    while True:
       try:
           product_user_input = input('> Please, type the number of the chosen product and press ENTER :')
       except ValueError:
           print('That\'s not a number!')
       else:
           if str(1) <= product_user_input <= str(4): # problème : trouver comment se baser sur la longueur de la liste
               break
           else:
               print('Out of range. You need to type a product number corresponding to the product list.')
    print(f'\nYou have chosen the following product : {product_list[category_user_input][product_user_input]}')


def main():
    print_categories()


if __name__ == "__main__":
    main()
