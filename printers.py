#! /usr/bin/env python3
# coding: utf-8


def print_cat_table(cat_table):
    """
    Prints out category table (cf. LIMIT)
    """
    cat_id = 1

    for category in cat_table:
        print(f"{cat_id} | {category[0]}")
        cat_id += 1


def print_products(product_list):
    """
    Prints out the products in the terminal with an index so user can later type a number
    to chose the products he desires to find a substitute for.
    """
    pdct_id = 1
    for pdct in product_list:
        print(f"{pdct_id} | {pdct[1]}")
        pdct_id += 1


def print_history(query1, query2):

    print("\n>> Your saved products : \n")

    i = 0
    while i < (len(query2)):
        for elem in query1:
            print(f"# date / time : {elem[6]} \n")
            print(f"\t## Your initial product : {query2[i][0]} "
                  f"\n\t\t# nutrition grade : {query2[i][1]} ")
            print(f"\n\t## Your substitute product : "
                  f"\n\t\t# barcode : {elem[0]} "
                  f"\n\t\t# substitute description : {elem[1]} "
                  f"\n\t\t# category : {elem[5]} "
                  f"\n\t\t# url : {elem[3]} "
                  f"\n\t\t# shop : {elem[4]} "
                  f"\n\t\t# nutrition grade : {elem[2]}\n "
                  f"\n ---------------------------------------------------------")
            i += 1